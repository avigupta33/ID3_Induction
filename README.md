# ID3 Induction
Implementation of ID3 Decision Tree Induction in Python

In this project, I sought to implement the ID3 machine learning algorithm in Python. The learning goals of this project 
were to develop a working understanding of decision tree induction. The implementation of the ID3 algorithm developed 
in this project sought to learn from a given training set, display a decision tree, and test the accuracy of the 
decision tree on the testing set. Individual data instances were parsed from the provided text files. Based on 
user-specified training and testing proportions, each instance was randomly assigned to either the training or the 
testing set using the random library. The ID3 algorithm was then applied to the training set to generate a decision tree, 
which was displayed using the displayTree helper function. The accuracy of the tree was assessed on the testing set 
using testTree, another helper function.
