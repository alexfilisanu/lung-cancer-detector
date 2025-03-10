import base64
import json
import os

import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST", "postgres-db"),
    database=os.getenv("POSTGRES_DB", "lung-cancer-db"),
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD", "postgres")
)
cursor = conn.cursor()


def get_user_id(email):
    try:
        cursor.execute("""
        SELECT id FROM users WHERE email = %s
        """, (email,))
        user_id = cursor.fetchone()

        return user_id[0] if user_id else None

    except Exception as e:
        print("Database error:", e)
        return None


@app.route('/insert-ct-prediction', methods=['POST'])
def insert_ct_prediction():
    try:
        image_file = request.files['image']
        user_id = get_user_id(request.form.get('user-email'))
        prediction_result = request.form.get('prediction')
        cursor.execute(
            """
            INSERT INTO predictions (user_id, prediction_result) VALUES (%s, %s) RETURNING id
            """, (user_id, prediction_result))
        prediction_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO ct_diagram_data (prediction_id, ct_diagram_photo) VALUES (%s, %s)
            """, (prediction_id, psycopg2.Binary(image_file.read())))

        conn.commit()

        return jsonify({'message': 'CT prediction inserted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/insert-survey-prediction', methods=['POST'])
def insert_survey_prediction():
    try:
        survey_data = request.json
        user_id = get_user_id(survey_data.pop('user-email', None))
        prediction_result = survey_data.pop('prediction', None)

        cursor.execute(
            """
            INSERT INTO predictions (user_id, prediction_result) VALUES (%s, %s) RETURNING id
            """, (user_id, prediction_result))
        prediction_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO survey_form_data (prediction_id, survey_form_data) VALUES (%s, %s)
            """, (prediction_id, json.dumps(survey_data)))

        conn.commit()

        return jsonify({'message': 'Survey prediction inserted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get-registrations', methods=['POST'])
def get_registrations():
    try:
        email = request.form.get('user-email')
        user_id = get_user_id(email)
        registrations = []

        if user_id is None:
            return jsonify({'error': 'User not found'}), 404

        cursor.execute("""
            SELECT 'ct' AS type, cd.ct_diagram_photo AS image, p.prediction_result AS result, p.timestamp
            FROM ct_diagram_data cd
            JOIN predictions p ON cd.prediction_id = p.id
            WHERE p.user_id = %s
            UNION ALL
            SELECT 'survey' AS type, '' AS image, p.prediction_result AS result, p.timestamp
            FROM predictions p
            JOIN survey_form_data sf ON p.id = sf.prediction_id
            WHERE p.user_id = %s
            ORDER BY timestamp DESC
            """, (user_id, user_id))

        for row in cursor.fetchall():
            registration = {
                'type': row[0],
                'image': base64.b64encode(row[1]).decode('utf-8') if row[0] == 'ct' else '',
                'result': row[2],
                'timestamp': row[3]
            }
            registrations.append(registration)
        return jsonify({'registrations': registrations}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/add-contact-form', methods=['POST'])
def add_contact_form():
    try:
        name = request.json.get('name')
        email = request.json.get('email')
        phone = request.json.get('phone')
        message = request.json.get('message')
        cursor.execute(
            """
            INSERT INTO contact_forms (name, phone, email, message) VALUES (%s, %s, %s, %s)
            """, (name, phone, email, message))
        conn.commit()

        return jsonify({'message': 'Contact form data inserted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=3050, host='0.0.0.0')
