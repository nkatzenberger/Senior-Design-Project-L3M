from huggingface_hub import HfApi, ModelCardData #ModelSearchArguments
api = HfApi()
models = api.list_models()
mdata = ModelCardData()
#newModel = ModelSearchArguments()
counter = 0
f = open("HuggingFaceModels.txt", "w")
for model in models: 
    if counter <50:
        model_info = api.model_info(model.modelId) 
        ID = str(model.modelId)
        splitID = ID.split('/')
        f.write(f"Publisher: {splitID[0]}\n")
        f.write(f"Model Name: {splitID[1]}\n") 
        f.write(f"https://huggingface.co/{model.modelId}\n")
        f.write(f"tags: {model_info.card_data.tags}\n\n")
        counter +=1
        
    else: 
        break
f.close()