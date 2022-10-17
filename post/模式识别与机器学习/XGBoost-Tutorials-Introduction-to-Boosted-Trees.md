创建于 2022-10-17
关键词: XGBoost, Boosted Trees.

This artical mainly referrence from https://xgboost.readthedocs.io/en/stable/tutorials/model.html.

XGBoost stands for “Extreme Gradient Boosting”, where the term “Gradient Boosting” originates from the paper *Greedy Function Approximation: A Gradient Boosting Machine*, by Friedman.

The **gradient boosted trees** has been around for a while, and there are a lot of materials on the topic. This tutorial will explain boosted trees in a self-contained and principled way using the elements of supervised learning. We think this explanation is cleaner, more formal, and motivates the model formulation used in XGBoost.

## Elements of Supervised Learning[](https://xgboost.readthedocs.io/en/stable/tutorials/model.html#elements-of-supervised-learning)

XGBoost is used for supervised learning problems, where we use the training data (with multiple features) $\boldsymbol x_i$ to predict a target variable $y_i$. Before we learn about trees specifically, let us start by reviewing the basic elements in supervised learning.

### Model and Parameters[](https://xgboost.readthedocs.io/en/stable/tutorials/model.html#model-and-parameters)

The **model** in supervised learning usually refers to the mathematical structure of by which the prediction $y_i$ is made from the input $\boldsymbol x_i$. A common example is a *linear model*, where the prediction is given as $y_i = \sum_j\theta_jx_{ij}$, a linear combination of weighted input features. The prediction value can have different interpretations, depending on the task, i.e., regression or classification. For example, it can be logistic transformed to get the probability of positive class in logistic regression, and it can also be used as a ranking score when we want to rank the outputs.

The **parameters** are the undetermined part that we need to learn from data. In linear regression problems, the parameters are the coefficients $\theta$. Usually we will use $\theta$ to denote the parameters (there are many parameters in a model, our definition here is sloppy).

### Objective Function: Training Loss + Regularization[](https://xgboost.readthedocs.io/en/stable/tutorials/model.html#objective-function-training-loss-regularization)

With judicious choices for $y_i$, we may express a variety of tasks, such as regression, classification, and ranking. The task of **training** the model amounts to finding the best parameters $\theta$ that best fit the training data $\boldsymbol x_i$ and labels $y_i$. In order to train the model, we need to define the **objective function** to measure how well the model fit the training data.

A salient characteristic of objective functions is that they consist two parts: **training loss** and **regularization term**:
$$
obj\left(\theta\right) = L\left(\theta\right) + \Omega\left(\theta\right)
$$
where $L$ is the training loss function, and $\Omega$ is the regularization term. The training loss measures how *predictive* our model is with respect to the training data. A common choice of $L$ is the *mean squared error*, which is given by
$$

$$
