import numpy as np
import joblib
from warnings import filterwarnings

# Suppress sklearn feature name warnings
filterwarnings("ignore", category=UserWarning, module="sklearn")


#Have the models folder and you dont it saves the models 
#position, # of Possessions, # of Defensive Possessions
def predict_epm(pos, Poss, O_Poss, off_values, def_values):
    # Load models based on position
    scaler_off = joblib.load(f"backend/EPM_Model/scaler_off_{pos}.pkl")
    pca_off = joblib.load(f"backend/EPM_Model/pca_off_{pos}.pkl")
    model_off = joblib.load(f"backend/EPM_Model/model_off_{pos}.pkl")

    scaler_def = joblib.load(f"backend/EPM_Model/scaler_def_{pos}.pkl")
    pca_def = joblib.load(f"backend/EPM_Model/pca_def_{pos}.pkl")
    model_def = joblib.load(f"backend/EPM_Model/model_def_{pos}.pkl")

    # Load y_off_pred and y_def_pred from training (assumed to be stored separately)
    y_off_pred = joblib.load(f"backend/EPM_Model/y_off_pred_{pos}.pkl")  # Load stored offensive predictions
    y_def_pred = joblib.load(f"backend/EPM_Model/y_def_pred_{pos}.pkl")  # Load stored defensive predictions

    if Poss == 0:
        Poss = 1
    if O_Poss == 0:
        O_Poss = 1

    #Convert off_values  and def_values to per 100 
    off_per100 = [0] * len(off_values)
    for index , value in enumerate(off_values):
        if not value:
            value = 0
        if index in [0,1,2,3,4,6,9,11]:
            off_per100[index] = 100 * (value/ Poss)
        else:
            off_per100[index] = 100 * (value/O_Poss)
    


    #['Def', 'STL', 'TO', 'PF', 'O_eFG_P', 'O_PTS']
    def_per100 = [0] * len(def_values)
    
    #def_values = ['Def', 'STL', 'TO', 'PF', 'O_FG_A', 'O_PTS']
    for index , value in enumerate(def_values):
        if not value:
            value = 0
        if index in [0,1,3,5]:
            def_per100[index] = 100 * (value/ O_Poss)
        elif index == 2:
            def_per100[index] = 100 * (value/Poss)
        else:
            if value == 0:
                def_per100[index] = 0
            else:
                def_per100[index] =  def_values[5] / (2* value) # O_efG (o_TS%)
        

    # Process offensive input
    off_val_np = np.array(off_per100).reshape(1, -1)
    off_input_scaled = scaler_off.transform(off_val_np)
    off_input_pca = pca_off.transform(off_input_scaled)
    obpm = model_off.predict(off_input_pca)[0]

    # Process defensive input
    def_val_np = np.array(def_per100).reshape(1, -1)
    def_input_scaled = scaler_def.transform(def_val_np)
    def_input_pca = pca_def.transform(def_input_scaled)
    dbpm = model_def.predict(def_input_pca)[0]

    # Compute mean and standard deviation from training predictions
    y_off_mean = np.mean(y_off_pred)
    y_off_std = np.std(y_off_pred)

    y_def_mean = np.mean(y_def_pred)
    y_def_std = np.std(y_def_pred)

    # Scaling the results
    target_mean, target_std = 0, 5  # Target scaling range

    obpm_scaled = ((obpm - y_off_mean) / y_off_std) * target_std + target_mean if y_off_std != 0 else target_mean
    dbpm_scaled = ((dbpm - y_def_mean) / y_def_std) * target_std + target_mean if y_def_std != 0 else target_mean
    
    dbpm_scaled *= -1 #Invert DBPM (- is bad + is good)

    bpm = obpm_scaled + dbpm_scaled

    return float(round(obpm_scaled, 1)), float(round(dbpm_scaled, 1)), float(round(bpm, 1))

'''
# Example usage
pos = "PG"
Poss = 52.7
O_Poss = 53.8
#off_features = ['PTS',  'FG_A', 'FT_A', '_3P_M', 'Off', 'Def', 'AST', 'STL', 'BLK', 'TO', 'PF', 'FD' ]
off_values = [31, 23, 0, 9, 0, 3, 3, 0, 0, 3, 3, 0]
#def_features = ['Def', 'STL', 'TO', 'PF', 'O_FG_A', 'O_PTS']
def_values = [3, 0, 3, 3, 14, 10]


print(predict_epm(pos,Poss, O_Poss, off_values,def_values))
'''