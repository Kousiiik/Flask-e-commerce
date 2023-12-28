from market import app, db
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm ,SellItemForm
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():  # put application's code here
    return render_template('home.html', title="home")


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form=SellItemForm()
    if request.method == "POST":
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f'congrats you purchased {p_item_object.name} for {p_item_object.price} ', category='success')
            else:
                flash(f'you don\'t have  enough balance to buy {p_item_object.name}', category='danger')
        sold_item=request.form.get('sold_item')
        sold_item_obj=Item.query.filter_by(name=sold_item).first()
        if sold_item_obj:
            if current_user.can_sell(sold_item_obj):
                sold_item_obj.sell(current_user)
                flash(f'congrats you have sold {sold_item_obj.name} for {sold_item_obj.price} and it back to market ', category='success')
            else:
                flash(f'something went wrong with {sold_item_obj.name}' , category='danger')

        return redirect(url_for('market_page'))
    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items=Item.query.filter_by(owner=current_user.id)

        return render_template('market.html', title='market', items=items, purchase_form=purchase_form , owned_items=owned_items , selling_form=selling_form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully!  , You are now logged in as {user_to_create.username}',
              category='success')
        return redirect(url_for('market_page'))
    if form.errors:
        for err in form.errors:
            flash(f'There is an error with creating a user {err}', category='danger')

    return render_template('register.html', form=form, title='register')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_login(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f' Success You are logged in as {attempted_user.username} ', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('user name and password are not match please try again ', categoty='danger')
    return render_template('login.html', form=form)


# we need to import logout_user
@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out', category='info')
    return redirect(url_for('home_page'))
