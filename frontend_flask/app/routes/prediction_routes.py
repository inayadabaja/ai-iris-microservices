from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.prediction_service import PredictionFrontendService

prediction_bp = Blueprint("prediction", __name__)
prediction_service = PredictionFrontendService()


@prediction_bp.route("/predict", methods=["GET", "POST"])
def predict():
    if "user_id" not in session:
        flash("Veuillez vous connecter", "warning")
        return redirect(url_for("auth.login"))

    prediction_result = None
    prediction_id = None
    submitted_values = None

    if request.method == "POST":
        try:
            payload = {
                "sepal_length": float(request.form.get("sepal_length")),
                "sepal_width": float(request.form.get("sepal_width")),
                "petal_length": float(request.form.get("petal_length")),
                "petal_width": float(request.form.get("petal_width"))
            }

            result = prediction_service.predict(payload)

            prediction_result = result.get("predicted_class")
            prediction_id = result.get("prediction_id")
            submitted_values = payload

            flash("Prédiction réalisée avec succès", "success")
        except Exception as e:
            flash(f"Erreur lors de la prédiction : {str(e)}", "danger")

    return render_template(
        "predict.html",
        prediction_result=prediction_result,
        prediction_id=prediction_id,
        submitted_values=submitted_values
    )


@prediction_bp.route("/feedback/<int:prediction_id>/<string:is_correct>", methods=["POST"])
def feedback(prediction_id, is_correct):
    if "user_id" not in session:
        flash("Veuillez vous connecter", "warning")
        return redirect(url_for("auth.login"))

    try:
        true_label = request.form.get("true_label", "").strip() or None

        payload = {
            "prediction_id": prediction_id,
            "is_correct": is_correct.lower() == "true",
            "true_label": true_label
        }

        prediction_service.send_feedback(payload)
        flash("Feedback envoyé avec succès", "success")
    except Exception as e:
        flash(f"Erreur lors de l'envoi du feedback : {str(e)}", "danger")

    return redirect(url_for("prediction.predict"))