# test
predicted = pd.DataFrame(model_rf.predict_proba(test_binary_dummy))
predicted.columns = ['Adoption', 'Died', 'Euthanasia', 'Return_to_owner', 'Transfer']
predicted.index += 1
predicted.index.name = 'ID'
