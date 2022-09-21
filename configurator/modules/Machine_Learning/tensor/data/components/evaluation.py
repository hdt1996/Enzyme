class Evaluation():
    def __init__(self):
        pass

class EvaluateKDS(Evaluation):
    def __init__(self, labels: list, **kwargs):
        self.labels = labels

    def predictEntries(self, model, data, num_entries: int = 5):
        for batch in data.take(num_entries):
            prediction=model.predict(x=batch[0])
            for index, value in enumerate(prediction):
                if value >= .5:
                    value = 1
                else:
                    value = 0
                pred_label = self.labels[value]
                act_label = self.labels[batch[1][index]]

                if pred_label == act_label:
                    print('Correct\n')
                else:
                    print('Wrong\n')
                #PLT.graphImage(data = batch[0][index], show = True)

class EvaluatePDF(Evaluation):
    def __init__(self):
        pass

class EvaluateNP(Evaluation):
    def __init__(self):
        pass