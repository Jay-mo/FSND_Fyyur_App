#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import os
import sys
import json
import dateutil.parser
import babel
from flask import (
    Flask, 
    render_template, 
    request, 
    Response, 
    flash, 
    redirect, 
    url_for, 
    abort
)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy.orm import backref, query_expression
from forms import *
# My Imports

from flask_migrate import Migrate
from datetime import datetime
from models import db, Venue, Artist, Shows
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
# db = SQLAlchemy(app)
db.init_app(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app, db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


# class Venue(db.Model):
#     __tablename__ = 'Venue'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     city = db.Column(db.String(120))
#     state = db.Column(db.String(120))
#     address = db.Column(db.String(120))
#     phone = db.Column(db.String(120))
#     image_link = db.Column(db.String(500))
#     facebook_link = db.Column(db.String(120))
#     # TODO: implement any missing fields, as a database migration using Flask-Migrate
#     # my edits
#     website_link = db.Column(db.String(120))
#     seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
#     seeking_description = db.Column(db.Text(), nullable=True)
#     genres = db.Column(db.ARRAY(db.String))
#     shows = db.relationship('Shows', backref='venue', lazy=True)


# class Artist(db.Model):
#     __tablename__ = 'Artist'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     city = db.Column(db.String(120))
#     state = db.Column(db.String(120))
#     phone = db.Column(db.String(120))
#     # genres = db.Column(db.String(120))
#     image_link = db.Column(db.String(500))
#     facebook_link = db.Column(db.String(120))

#     # TODO: implement any missing fields, as a database migration using Flask-Migrate
#     # my edits
#     seeking_venue = db.Column(db.Boolean(), nullable=False, default=False)
#     seeking_description = db.Column(db.Text(), nullable=True)
#     genres = db.Column(db.ARRAY(db.String))
#     website_link = db.Column(db.String(120))

#     shows = db.relationship('Shows', backref='artist', lazy=True)
# # TODO Implement Show and Artist models, and complete all model
# # relationships and properties, as a database migration.


# class Shows(db.Model):
#     __tablename__ = 'Shows'
#     id = db.Column(db.Integer, primary_key=True)
#     venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
#     artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
#     start_time = db.Column(db.DateTime)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime


def get_upcoming_shows(shows):
    count = 0

    for show in shows:
        if show.start_time > datetime.now():
            count += 1

        return count

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    # data=[{
    #   "city": "San Francisco",
    #   "state": "CA",
    #   "venues": [{
    #     "id": 1,
    #     "name": "The Musical Hop",
    #     "num_upcoming_shows": 0,
    #   }, {
    #     "id": 3,
    #     "name": "Park Square Live Music & Coffee",
    #     "num_upcoming_shows": 1,
    #   }]
    # }, {
    #   "city": "New York",
    #   "state": "NY",
    #   "venues": [{
    #     "id": 2,
    #     "name": "The Dueling Pianos Bar",
    #     "num_upcoming_shows": 0,
    #   }]
    # }]
    data = []
    all_venues = Venue.query.all()

    unique_geo_location = Venue.query.distinct(Venue.city, Venue.state).all()

    for location in unique_geo_location:
        data.append({
            "city": location.city,
            "state": location.state,
            "venues": [{'id': venue.id, 'name': venue.name, 'num_upcoming_shows': get_upcoming_shows(venue.shows)}
                       for venue in all_venues
                       if venue.state == location.state and venue.city == location.city]
        })

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    # response={
    #   "count": 1,
    #   "data": [{
    #     "id": 2,
    #     "name": "The Dueling Pianos Bar",
    #     "num_upcoming_shows": 0,
    #   }]
    # }

    search_term = request.form.get('search_term', '')
    search_results = Venue.query.filter(
        Venue.name.ilike('%{}%'.format(search_term)))
    data = []
    count = 0
    num_upcoming_shows = 0
    for venue in search_results:
        # for show in venue.shows:
        #   if show.start_time > datetime.datetime.now():
        #     num_upcoming_shows += 1
        data.append({'id': venue.id, 'name': venue.name,
                    "num_upcoming_shows": get_upcoming_shows(venue.shows)})
        count += 1

    response = {
        'count': count,
        'data': data
    }
    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    # data1={
    #   "id": 1,
    #   "name": "The Musical Hop",
    #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    #   "address": "1015 Folsom Street",
    #   "city": "San Francisco",
    #   "state": "CA",
    #   "phone": "123-123-1234",
    #   "website": "https://www.themusicalhop.com",
    #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
    #   "seeking_talent": True,
    #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    #   "past_shows": [{
    #     "artist_id": 4,
    #     "artist_name": "Guns N Petals",
    #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    #     "start_time": "2019-05-21T21:30:00.000Z"
    #   }],
    #   "upcoming_shows": [],
    #   "past_shows_count": 1,
    #   "upcoming_shows_count": 0,
    # }
    # data2={
    #   "id": 2,
    #   "name": "The Dueling Pianos Bar",
    #   "genres": ["Classical", "R&B", "Hip-Hop"],
    #   "address": "335 Delancey Street",
    #   "city": "New York",
    #   "state": "NY",
    #   "phone": "914-003-1132",
    #   "website": "https://www.theduelingpianos.com",
    #   "facebook_link": "https://www.facebook.com/theduelingpianos",
    #   "seeking_talent": False,
    #   "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    #   "past_shows": [],
    #   "upcoming_shows": [],
    #   "past_shows_count": 0,
    #   "upcoming_shows_count": 0,
    # }
    # data3={
    #   "id": 3,
    #   "name": "Park Square Live Music & Coffee",
    #   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    #   "address": "34 Whiskey Moore Ave",
    #   "city": "San Francisco",
    #   "state": "CA",
    #   "phone": "415-000-1234",
    #   "website": "https://www.parksquarelivemusicandcoffee.com",
    #   "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    #   "seeking_talent": False,
    #   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #   "past_shows": [{
    #     "artist_id": 5,
    #     "artist_name": "Matt Quevedo",
    #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    #     "start_time": "2019-06-15T23:00:00.000Z"
    #   }],
    #   "upcoming_shows": [{
    #     "artist_id": 6,
    #     "artist_name": "The Wild Sax Band",
    #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #     "start_time": "2035-04-01T20:00:00.000Z"
    #   }, {
    #     "artist_id": 6,
    #     "artist_name": "The Wild Sax Band",
    #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #     "start_time": "2035-04-08T20:00:00.000Z"
    #   }, {
    #     "artist_id": 6,
    #     "artist_name": "The Wild Sax Band",
    #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #     "start_time": "2035-04-15T20:00:00.000Z"
    #   }],
    #   "past_shows_count": 1,
    #   "upcoming_shows_count": 1,
    # }
    #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]

    # venue = Venue.query.get(venue_id)

    data = Venue.query.get(venue_id)

    if data is None:
        abort(404)
    else:
        data.upcoming_shows = []
        data.past_shows = []
        data.upcoming_shows_count = 0
        data.past_shows_count = 0

        past_shows_query = db.session.query(Shows).join(Venue).filter(
            Shows.venue_id == venue_id).filter(
            Shows.start_time < datetime.now()).all()
        upcoming_shows_query = db.session.query(Shows).join(Venue).filter(
            Shows.venue_id == venue_id).filter(
            Shows.start_time > datetime.now()).all()

        for show in upcoming_shows_query:

            data.upcoming_shows.append({
                "artist_id": show.artist_id,
                "artist_name": show.artist.name,
                "artist_image_link": show.artist.image_link,
                "start_time": show.start_time.strftime("%d/%m/%Y, %H:%M")
            })

        data.upcoming_shows_count = len(upcoming_shows_query)

        for show in past_shows_query:
            data.past_shows.append({
                "artist_id": show.artist_id,
                "artist_name": show.artist.name,
                "artist_image_link": show.artist.image_link,
                "start_time": show.start_time.strftime("%d/%m/%Y, %H:%M")
            })

        data.past_shows_count = len(past_shows_query)

        # for show in data.shows:
        #   if show.start_time >= datetime.datetime.now():
        #     data.upcoming_shows.append({
        #       "artist_id": show.artist_id,
        #       "artist_name": show.artist.name,
        #       "artist_image_link": show.artist.image_link,
        #       "start_time": show.start_time.strftime("%d/%m/%Y, %H:%M")
        #     })
        #     data.upcoming_shows_count += 1

        #   else:
        #     data.past_shows.append({
        #       "artist_id": show.artist_id,
        #       "artist_name": show.artist.name,
        #       "artist_image_link": show.artist.image_link,
        #       "start_time": show.start_time.strftime("%d/%m/%Y, %H:%M")
        #     })
        #     data.past_shows_count += 1
        return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    form = VenueForm(request.form)
    try:

        new_venue = Venue()
        form.populate_obj(new_venue)
        # new_venue = Venue(
        #     name=form.name.data,
        #     city=form.city.data,
        #     state=form.state.data,
        #     address=form.address.data,
        #     phone=form.phone.data,
        #     image_link=form.image_link.data,
        #     genres=form.genres.data,
        #     facebook_link=form.facebook_link.data,
        #     website_link=form.website_link.data
        # )
        # new_venue.name = request.form.get('name')
        # new_venue.city = request.form.get('city')
        # new_venue.state = request.form.get('state')
        # new_venue.address = request.form.get('address')
        # new_venue.phone = request.form.get('phone')
        # new_venue.image_link = request.form.get('image_link')
        # new_venue.genres = request.form.getlist('genres')
        # new_venue.facebook_link = request.form.get('facebook_link')
        # new_venue.website_link = request.form.get('website_link')
        # if request.form.get('seeking_talent') == 'y':
        # if form.seeking_talent.data == 'y':
        #     new_venue.seeking_talent = True
        #     # new_venue.seeking_description = request.form.get(
        #     #     'seeking_description')
        #     new_venue.seeking_description = form.seeking_description.data
        # else:
        #     new_venue.seeking_talent = False

        db.session.add(new_venue)
        db.session.commit()

        # on successful db insert, flash success
        flash('Venue ' + new_venue.name + ' was successfully listed!')

    except BaseException:
        db.session.rollback()
        print(sys.exc_info())

        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Venue ' + data.name + ' could not be
        # listed.')
        flash('An error occurred. Venue ' +
              new_venue.name + ' could not be listed.')
    finally:
        db.session.close()

    # on successful db insert, flash success
    # flash('Venue ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>/delete', methods=['POST'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit
    # could fail.

    try:
        delete_venue = Venue.query.get(venue_id)
        db.session.delete(delete_venue)
        db.session.commit()

        flash('Venue ' + delete_venue.name + ' was successfully deleted!')
    except BaseException:
        db.session.rollback()
        print(sys.exc_info())

        flash('Venue ' + delete_venue.name + ' could not be deleted!')

    finally:
        db.session.close()
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the
    # homepage
    return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    # data=[{
    #   "id": 4,
    #   "name": "Guns N Petals",
    # }, {
    #   "id": 5,
    #   "name": "Matt Quevedo",
    # }, {
    #   "id": 6,
    #   "name": "The Wild Sax Band",
    # }]
    data = []
    artists_results = Artist.query.with_entities(Artist.id, Artist.name)

    for id, name in artists_results:
        data.append({'id': id, 'name': name})
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".

    search_term = request.form.get('search_term', '')
    search_results = Artist.query.filter(
        Artist.name.ilike('%{}%'.format(search_term)))
    data = []

    for artist in search_results:
        data.append({'id': artist.id, 'name': artist.name})

    response = {
        "count": search_results.count(),
        "data": data
    }
    return render_template('pages/search_artists.html',
                           results=response, search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id
    # data1={
    #   "id": 4,
    #   "name": "Guns N Petals",
    #   "genres": ["Rock n Roll"],
    #   "city": "San Francisco",
    #   "state": "CA",
    #   "phone": "326-123-5000",
    #   "website": "https://www.gunsnpetalsband.com",
    #   "facebook_link": "https://www.facebook.com/GunsNPetals",
    #   "seeking_venue": True,
    #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    #   "past_shows": [{
    #     "venue_id": 1,
    #     "venue_name": "The Musical Hop",
    #     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    #     "start_time": "2019-05-21T21:30:00.000Z"
    #   }],
    #   "upcoming_shows": [],
    #   "past_shows_count": 1,
    #   "upcoming_shows_count": 0,
    # }
    # data2={
    #   "id": 5,
    #   "name": "Matt Quevedo",
    #   "genres": ["Jazz"],
    #   "city": "New York",
    #   "state": "NY",
    #   "phone": "300-400-5000",
    #   "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    #   "seeking_venue": False,
    #   "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    #   "past_shows": [{
    #     "venue_id": 3,
    #     "venue_name": "Park Square Live Music & Coffee",
    #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #     "start_time": "2019-06-15T23:00:00.000Z"
    #   }],
    #   "upcoming_shows": [],
    #   "past_shows_count": 1,
    #   "upcoming_shows_count": 0,
    # }
    # data3={
    #   "id": 6,
    #   "name": "The Wild Sax Band",
    #   "genres": ["Jazz", "Classical"],
    #   "city": "San Francisco",
    #   "state": "CA",
    #   "phone": "432-325-5432",
    #   "seeking_venue": False,
    #   "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #   "past_shows": [],
    #   "upcoming_shows": [{
    #     "venue_id": 3,
    #     "venue_name": "Park Square Live Music & Coffee",
    #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #     "start_time": "2035-04-01T20:00:00.000Z"
    #   }, {
    #     "venue_id": 3,
    #     "venue_name": "Park Square Live Music & Coffee",
    #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #     "start_time": "2035-04-08T20:00:00.000Z"
    #   }, {
    #     "venue_id": 3,
    #     "venue_name": "Park Square Live Music & Coffee",
    #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    #     "start_time": "2035-04-15T20:00:00.000Z"
    #   }],
    #   "past_shows_count": 0,
    #   "upcoming_shows_count": 3,
    # }
    # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]

    data = Artist.query.get(artist_id)

    if data is None:
        abort(404)

    else:
        data.upcoming_shows = []
        data.past_shows = []
        data.upcoming_shows_count = 0
        data.past_shows_count = 0

        past_shows_query = db.session.query(Shows).join(Artist).filter(
            Shows.artist_id == artist_id).filter(
            Shows.start_time < datetime.now()).all()
        upcoming_shows_query = db.session.query(Shows).join(Artist).filter(
            Shows.artist_id == artist_id).filter(
            Shows.start_time > datetime.now()).all()

        for show in upcoming_shows_query:

            data.upcoming_shows.append({
                "venue_id": show.venue_id,
                "venue_name": show.venue.name,
                "venue_image_link": show.venue.image_link,
                "start_time": show.start_time.strftime("%d/%m/%Y, %H:%M")
            })

        data.upcoming_shows_count = len(upcoming_shows_query)

        for show in past_shows_query:
            data.past_shows.append({
                "venue_id": show.venue_id,
                "venue_name": show.venue.name,
                "venue_image_link": show.venue.image_link,
                "start_time": show.start_time.strftime("%d/%m/%Y, %H:%M")
            })

        data.past_shows_count = len(past_shows_query)

        # for show in data.shows:
        #   if show.start_time > datetime.datetime.now():
        #     data.upcoming_shows.append({
        #       "venue_id": show.venue_id,
        #       "venue_name": show.venue.name,
        #       "venue_image_link": show.venue.image_link,
        #       "start_time": show.start_time.strftime("%d/%m/%Y, %H:%M")
        #     })
        #     data.upcoming_shows_count += 1

        #   else:
        #     data.past_shows.append({
        #       "venue_id": show.venue_id,
        #       "venue_name": show.venue.name,
        #       "venue_image_link": show.venue.image_link,
        #       "start_time": show.start_time.strftime("%d/%m/%Y, %H:%M")
        #     })
        #     data.past_shows_count += 1

        return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm(obj=artist)
    # artist={
    #   "id": 4,
    #   "name": "Guns N Petals",
    #   "genres": ["Rock n Roll"],
    #   "city": "San Francisco",
    #   "state": "CA",
    #   "phone": "326-123-5000",
    #   "website": "https://www.gunsnpetalsband.com",
    #   "facebook_link": "https://www.facebook.com/GunsNPetals",
    #   "seeking_venue": True,
    #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
    # }
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    try:
        edit_artist = Artist.query.get(artist_id)
        # print(edit_artist.seeking_venue)

        # print(request.form)
        edit_artist.name = request.form.get('name')
        edit_artist.city = request.form.get('city')
        edit_artist.state = request.form.get('state')
        edit_artist.phone = request.form.get('phone')
        edit_artist.image_link = request.form.get('image_link')
        edit_artist.genres = request.form.getlist('genres')
        edit_artist.facebook_link = request.form.get('facebook_link')
        edit_artist.website_link = request.form.get('website_link')

        if request.form.get('seeking_venue') == 'y':
            edit_artist.seeking_venue = True
            edit_artist.seeking_description = request.form.get(
                'seeking_description')
        else:
            edit_artist.seeking_venue = False

        print(edit_artist.seeking_venue)
        db.session.add(edit_artist)
        db.session.commit()

        # on successful db insert, flash success
        flash('Artist ' + edit_artist.name + ' was successfully edited!')
    except BaseException:
        db.session.rollback()
        flash('An error occurred. Artist ' +
              edit_artist.name + ' could not be edited.')
        print(sys.exc_info())
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm(obj=venue)
    # venue={
    #   "id": 1,
    #   "name": "The Musical Hop",
    #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    #   "address": "1015 Folsom Street",
    #   "city": "San Francisco",
    #   "state": "CA",
    #   "phone": "123-123-1234",
    #   "website": "https://www.themusicalhop.com",
    #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
    #   "seeking_talent": True,
    #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    # }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes

    try:
        edit_venue = Venue.query.get(venue_id)

        edit_venue.name = request.form.get('name')
        edit_venue.city = request.form.get('city')
        edit_venue.state = request.form.get('state')
        edit_venue.address = request.form.get('address')
        edit_venue.phone = request.form.get('phone')
        edit_venue.image_link = request.form.get('image_link')
        edit_venue.genres = request.form.getlist('genres')
        edit_venue.facebook_link = request.form.get('facebook_link')
        edit_venue.website_link = request.form.get('website_link')

        if request.form.get('seeking_talent') == 'y':
            edit_venue.seeking_talent = True
            edit_venue.seeking_description = request.form.get(
                'seeking_description')
        else:
            edit_venue.seeking_talent = False

        db.session.add(edit_venue)
        db.session.commit()

        # on successful db insert, flash success
        flash('venue ' + edit_venue.name + ' was successfully edited!')
    except BaseException:
        db.session.rollback()
        flash('An error occurred. venue ' +
              edit_venue.name + ' could not be edited.')
        print(sys.exc_info())
    finally:
        db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # request.form.getlist
    form=ArtistForm(request.form)

    try:
        new_artist = Artist()
        form.populate_obj(new_artist)
        # new_artist.name = request.form.get('name')
        # new_artist.city = request.form.get('city')
        # new_artist.state = request.form.get('state')
        # new_artist.phone = request.form.get('phone')
        # new_artist.image_link = request.form.get('image_link')
        # new_artist.genres = request.form.getlist('genres')
        # new_artist.facebook_link = request.form.get('facebook_link')
        # new_artist.website_link = request.form.get('website_link')
        # new_artist.seeking_venue = request.form.get('seeking_venue')
        # new_artist.seeking_description = request.form.get(
        #     'seeking_description')
        db.session.add(new_artist)
        db.session.commit()

        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except BaseException:
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Artist ' + data.name + ' could not be
        # listed.')
        db.session.rollback()
        flash('An error occurred. Artist ' +
              new_artist.name + ' could not be listed.')
    finally:
        db.session.close()

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    # data=[{
    #   "venue_id": 1,
    #   "venue_name": "The Musical Hop",
    #   "artist_id": 4,
    #   "artist_name": "Guns N Petals",
    #   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    #   "start_time": "2019-05-21T21:30:00.000Z"
    # }, {
    #   "venue_id": 3,
    #   "venue_name": "Park Square Live Music & Coffee",
    #   "artist_id": 5,
    #   "artist_name": "Matt Quevedo",
    #   "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    #   "start_time": "2019-06-15T23:00:00.000Z"
    # }, {
    #   "venue_id": 3,
    #   "venue_name": "Park Square Live Music & Coffee",
    #   "artist_id": 6,
    #   "artist_name": "The Wild Sax Band",
    #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #   "start_time": "2035-04-01T20:00:00.000Z"
    # }, {
    #   "venue_id": 3,
    #   "venue_name": "Park Square Live Music & Coffee",
    #   "artist_id": 6,
    #   "artist_name": "The Wild Sax Band",
    #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #   "start_time": "2035-04-08T20:00:00.000Z"
    # }, {
    #   "venue_id": 3,
    #   "venue_name": "Park Square Live Music & Coffee",
    #   "artist_id": 6,
    #   "artist_name": "The Wild Sax Band",
    #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    #   "start_time": "2035-04-15T20:00:00.000Z"
    # }]

    data = []

    all_shows = Shows.query.all()

    for show in all_shows:

        data.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time.strftime("%d/%m/%Y, %H:%M")
        })
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    form = ShowForm(request.form)
    try:
        new_show = Shows()
        form.populate_obj(new_show)

        # new_show.artist_id = request.form.get('artist_id')
        # new_show.venue_id = request.form.get('venue_id')
        # new_show.start_time = request.form.get('start_time')

        db.session.add(new_show)
        db.session.commit()

        # on successful db insert, flash success
        flash('Show was successfully listed!')
    except BaseException:
        db.session.rollback()
        print(sys.exc_info())

        # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')

        flash('An error occurred. Show could not be listed.')

    finally:
        db.session.close()

    # on successful db insert, flash success
    flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
# if __name__ == '__main__':
#     app.run()

# Or specify port manually:

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
