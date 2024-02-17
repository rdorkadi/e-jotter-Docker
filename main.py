from website import create_app
import os
from flask_recaptcha import ReCaptcha # Import ReCaptcha object


app = create_app()


# app = Flask(__name__)
app.config['RECAPTCHA_SITE_KEY'] = '' # <-- Add your site key
app.config['RECAPTCHA_SECRET_KEY'] = '' # <-- Add your secret key
recaptcha = ReCaptcha(app) # Create a ReCaptcha object by passing in 'app' as parameter


if __name__ == '__main__':
    port = int(os.environ.get("PORT","5001"))
    app.run(host='0.0.0.0',port=port,debug=True)
    #app.run(port=5003, debug=True)
