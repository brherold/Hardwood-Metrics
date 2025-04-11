import numpy as np
import joblib
import warnings
warnings.filterwarnings("ignore", message="X does not have valid feature names.*")


#Have the models folder and you dont it saves the models 

def predict_bpm(pos, Poss, O_Poss, off_values, def_values):
    # Load models based on position
    scaler_off = joblib.load(f"backend/BPM_Model/scaler_off_{pos}.pkl")
    pca_off = joblib.load(f"backend/BPM_Model/pca_off_{pos}.pkl")
    model_off = joblib.load(f"backend/BPM_Model/model_off_{pos}.pkl")

    scaler_def = joblib.load(f"backend/BPM_Model/scaler_def_{pos}.pkl")
    pca_def = joblib.load(f"backend/BPM_Model/pca_def_{pos}.pkl")
    model_def = joblib.load(f"backend/BPM_Model/model_def_{pos}.pkl")

    # Load y_off_pred and y_def_pred from training (assumed to be stored separately)
    y_off_pred = joblib.load(f"backend/BPM_Model/y_off_pred_{pos}.pkl")  # Load stored offensive predictions
    y_def_pred = joblib.load(f"backend/BPM_Model/y_def_pred_{pos}.pkl")  # Load stored defensive predictions




    #If player played in game but played "0" possessisons (played 1 minute)
    if Poss == 0:
        Poss = 1
    if O_Poss == 0:
        O_Poss = 1
    
    #off values -> [PTS, FGA, FTA, Off, AST, TO, FD]
    off_per100 = []


    try:
        TS = off_values[0] / (2*(off_values[1] + .44*off_values[2]))
    except:
        TS = 0

    #Converting off_values and def_values to per 100 and proper format for model
    for index, value in enumerate(off_values):
        if index in [0,3,4,5,6]:
            off_per100.append(100 * value / Poss)

    #off_per100 = ['PTS', 'Off', 'AST', 'TO', 'FD', 'TS%']
    off_per100.append(TS)

    
    #def values -> [OPTS, OFGA, Def, STL, PF]
    def_per100 = []

    try:
        O_efG = def_values[0]/ (2* def_values[1]) #efg same as TS when no FTAs
    except:
        O_efG = 0

    for index, value in enumerate(def_values):
        if index != 1:
            def_per100.append(100 * value / O_Poss)
    

    #def_per100 = [OPTS,DReb,STL,PF,OeFG%]
    def_per100.append(O_efG)
    

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
    bpm = obpm_scaled + dbpm_scaled

    return float(round(obpm_scaled, 1)), float(round(dbpm_scaled, 1)), float(round(bpm, 1))

'''
# Example usage
pos = "SG"
Poss = 60
O_Poss = 50
#off_values = [PTS, FGA, FTA, Off, AST, TO, FD]
off_values = [22, 18, 4, 1, 5, 2, 3]
#def_values = [OPTS, OFGA, Def, STL, PF]
def_values = [18, 16, 3, 2, 2]



print(predict_bpm(pos,Poss,O_Poss,off_values,def_values))
'''

