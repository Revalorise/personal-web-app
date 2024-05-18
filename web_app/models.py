from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from web_app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc))

    stocks: so.WriteOnlyMapped['StockData'] = so.relationship(
        back_populates='owner')

    @login.user_loader
    def load_user(id):
        return db.session.get(User, int(id))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class StockData(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    date: so.Mapped[datetime]
    open: so.Mapped[float]
    high: so.Mapped[float]
    dividends: so.Mapped[float]
    stock_splits:  so.Mapped[float]

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('User.id'),
                                              index=True)

    owner: so.Mapped[User] = so.relationship(back_populates='stocks')

    @login.user_loader
    def load_user(id):
        return db.session.get(User, int(id))


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')


class RegisteringStockData(FlaskForm):
    ticker = StringField('Ticker', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_ticker(self, ticker):
        stock = db.session.scalar(sa.select(Stock).where(
            Stock.ticker == ticker.data))
        if stock is not None:
            raise ValidationError('Please use a different ticker.')