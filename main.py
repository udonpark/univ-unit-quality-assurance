from flask import Flask, flash
from flask import render_template
from flask import request
from app.calculator import *

from app.calculator_form import *
import os
SECRET_KEY = os.urandom(32)

ev_calculator_app = Flask(__name__)
ev_calculator_app.config['SECRET_KEY'] = SECRET_KEY


@ev_calculator_app.route('/', methods=['GET', 'POST'])
def operation_result():
    # request.form looks for:
    # html tags with matching "name="

    calculator_form = Calculator_Form(request.form)
    # validation of the form
    if request.method == "POST" and calculator_form.validate():
        # if valid, create calculator to calculate the time and cost
        calculator = Calculator()

        # extract information from the form
        battery_capacity = request.form['BatteryPackCapacity']
        initial_charge = request.form['InitialCharge']
        final_charge = request.form['FinalCharge']
        start_date = request.form['StartDate']
        start_time = request.form['StartTime']
        charger_configuration = request.form['ChargerConfiguration']
        postcode = request.form['PostCode']

        # you may change the logic as your like
        duration = calculator.charge_time(final_charge, initial_charge, battery_capacity, calculator.get_power(charger_configuration))

        is_peak = calculator.is_peak(start_time)

        # if is_peak:
        #     peak_period = calculator.peak_period(start_date)

        is_holiday = calculator.is_holiday(start_date)

        # cost = calculator.cost_calculation(initial_charge, final_charge, battery_capacity, is_peak, is_holiday)
        #
        # time = calculator.time_calculation(initial_charge, final_charge, battery_capacity, power)

        # This is to convert dd/mm/yyyy to dd-mm-yyyy from the input
        temp_date = start_date.split("/")
        start_date = temp_date[0] + "-" + temp_date[1] + "-" + temp_date[2]
        cost = calculator.calculate_charging_cost(start_date, start_time, postcode, final_charge, initial_charge,
                                                  battery_capacity, calculator.get_power(charger_configuration), charger_configuration)

        time = calculator.charge_time(final_charge, initial_charge, battery_capacity, calculator.get_power(charger_configuration))
        # you may change the return statement also
        
        # values of variables can be sent to the template for rendering the webpage that users will see
        return render_template('calculator.html', cost=cost, time=time, calculation_success=True, form=calculator_form)
        # return render_template('calculator.html', calculation_success=True, form=calculator_form)

    else:
        # battery_capacity = request.form['BatteryPackCapacity']
        # flash(battery_capacity)
        # flash("something went wrong")
        flash_errors(calculator_form)
        return render_template('calculator.html', calculation_success=False, form=calculator_form)

# method to display all errors
def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')


if __name__ == '__main__':
    ev_calculator_app.run()