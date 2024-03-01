from flask import Flask, render_template, flash, redirect, url_for, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

# Create Flask app
app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# Initialize SQLAlchemy and connect to database.
connect_db(app)

# Configure Debug Toolbar
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

# Seed database
from seed import seed_database
with app.app_context():
    seed_database()

# Routes
@app.route('/')
def list_pets():
    """List all pets."""
    pets = Pet.query.all()
    return render_template("/pets/pet_list.html", pets=pets)

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""
    return render_template('404.html'), 404

@app.route("/pets/add", methods=["GET", "POST"])
def add_pet():
    """Add a pet."""
    form = AddPetForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        print("Form data", data)
        try:
            new_pet = Pet(**data)
            db.session.add(new_pet)
            db.session.commit()
            flash(f"{new_pet.name} added.")

            # Store the new_pet id in the session
            session['new_pet_id'] = new_pet.id
            return redirect(url_for('list_pets'))
        except Exception as e:
            print("Error committing to database:", e)  # Print any database commit errors
            db.session.rollback()  # Rollback transaction in case of error
            flash("Error adding pet. Please try again.", "error")
    else:
        print("Form validation failed:", form.errors)  # Print form validation errors

    return render_template("/pets/add.html", form=form)

@app.route("/pets/<int:pet_id>", methods=["GET", "POST"])
def edit_pet(pet_id):
    """Edit pet."""
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data
        db.session.commit()
        flash(f"{pet.name} updated.")
        return redirect(url_for('list_pets'))

    return render_template("/pets/edit.html", form=form, pet=pet)

@app.route("/api/pets/<int:pet_id>", methods=['GET'])
def api_get_pet(pet_id):
    """Return basic info about pet in JSON."""
    pet = Pet.query.get_or_404(pet_id)
    info = {"name": pet.name, "age": pet.age}
    return jsonify(info)

# Run the application if executed directly
if __name__ == '__main__':
    # Create all database tables
    with app.app_context():
        db.create_all()
    # Run the Flask app
    app.run(debug=True)
