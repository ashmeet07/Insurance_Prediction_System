import pandas as pd
import pickle

with open("model/model.pkl","rb") as f:
    model = pickle.load(f)


class_labels=model.classes_.tolist()

def predict_output(user_input:dict):
    input_df=pd.DataFrame([user_input])
    prediction= model.predict(input_df)[0]
    probablities=model.predict_proba(input_df)[0]
    confidence_score=max(probablities)

    class_probabs=dict(zip(class_labels,map(lambda p :round(p,4),probablities)))

    return{
            "predicted_category":prediction,
            "confidence": round(confidence_score,4),
            "class_probablities":class_probabs
    } 