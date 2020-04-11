import elements
import simulation_tools
import src.test_tools
import sklearn

#from sklearn import linear_model

if __name__ == '__main__':
    basic_project = src.test_tools.project_setup()

    training_labels, training_sample = simulation_tools.LabelStudy.generate_multiple_labels(basic_project,
                                                                                            "MidProject", 51, 1000)


    model = sklearn.linear_model.LogisticRegression()
    model.fit(training_sample, training_labels)
    print("Logistic Regression: Training set learned")

    predictedLabels = model.predict(training_sample)
    simulation_tools.LabelStudy.generate_results(predictedLabels, training_labels)







