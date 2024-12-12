from huggingface_hub import HfApi, ModelCardData #ModelSearchArguments
api = HfApi()
models = api.list_models()
mdata = ModelCardData()
#newModel = ModelSearchArguments()
counter = 0
for model in models: 
    if counter <5:
        model_info = api.model_info(model.modelId) 
        ID = str(model.modelId)
        splitID = ID.split('/')
        print(f"Publisher: {splitID[0]}")
        print(f"Model Name: {splitID[1]}") 
        print(f"https://huggingface.co/{model.modelId}")
        print(f"tags: {model_info.card_data.tags}\n")
        counter +=1
        
    else: 
        break