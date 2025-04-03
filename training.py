# Training the Model
import tensorflow as tf
import pandas as pd
import numpy as np
from tensorflow.keras import layers, models, Model
from tensorflow.keras.datasets import mnist
import sklearn
import matplotlib.pyplot as plt
import ast


from sklearn.model_selection import train_test_split
# X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)

data = pd.read_csv("climbs.csv")
#data = pd.read_csv("climbs_clean.csv")
data = data.drop(columns=["Name", "Setter"])
#data = data.drop(columns=["Name", "Setter", "Ascensionist Count"])
data["Holds"] = data["Holds"].apply(ast.literal_eval)
#print(X)
#for index, climb in data.iterrows():
def gen_image(holds):
  #holds = climb[2]
  board = np.zeros((45, 45)) #[[0] * 40] * 40
  #print(holds)
  for (x, y), typ in holds:
    #print(f"hold: {hold}\n", flush=True)
    #hold = hold.split(", ")
    #x = int(hold[0][1:])
    #y = int(hold[1][:-1])
    #typ = hold[2]
    x //= 4
    y //= 4
    val = 0.1
    #print(x, y)
    #print(typ)
    #print(type(typ))
    if typ == "'Hand'":
        val = 1
    if typ == "'Feet'":
        val = 0.25
    if typ == "'Starting'":
        val = 0.5
    if typ == "'Finish'":
        val = 0.75
    board[x][y] = val
  #print(board)
  #data.loc[index, "Holds"] = board
  return board

data["Holds"] = data["Holds"].apply(gen_image)



X = data.drop(columns=["V Grade"])
#y = data["V Grade"]

#X = [np.array(data["Holds"]), data["Angle"]]
#for d in data["Holds"]:
#  X.append(np.array(d))
y = np.array(data["V Grade"])
#for d in data["V Grade"]:
#  y.append(np.array(d))

print(X)



#X.describe()
#y.describe()

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)

print("\n\n\n\n\n\n\n")
#(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.cifar10.load_data()
#(X_train,y_train) , (X_test,y_test)=mnist.load_data()

#train_images, test_images = train_images / 255.0, test_images / 255.0
#print(X_train.shape)
#print(X_val.shape)
#X.describe()
#y.describe()
#print(f"X_train at pos 0: {X_train[0]}")

# flatten
ang_train = X_train["Angle"]
X_train = np.array(X_train["Holds"])

ang_val = X_val["Angle"]
X_val = np.array(X_val["Holds"])

train_size = X_train.shape[0]
val_size = X_val.shape[0]
X_train = np.concatenate(X_train)
X_val = np.concatenate(X_val)

X_train = X_train.reshape((train_size, 45, 45, 1))
X_val = X_val.reshape((val_size, 45, 45,1))



print(type(X_train))
print(type(y_train))
print(X_train.shape)
print(X_val.shape)

#X_train=X_train/255
#X_val=X_val/255


#print(y_train)

inputs = layers.Input(shape=(45, 45, 1), name="holds")

input2 = layers.Input((1,), name="angle")
ang = layers.Dense(10, activation="relu")(input2)

at1 = layers.AveragePooling2D((3, 3), strides=2)(inputs)
at2 = layers.Conv2D(128, (12, 12), activation="relu")(inputs)
at3 = layers.MaxPooling2D((6,6))(at2)

at4 = layers.Conv2D(32, (3, 3), activation="relu")(at1)
at4 = layers.MaxPooling2D((2,2))(at4)

at5 = layers.Conv2D(64, (10, 5), activation="relu", strides=(5,2))(inputs)
at6 = layers.Conv2D(64, (5, 10), activation="relu", strides=(2,5))(inputs)

a1 = layers.Flatten()(at3)
a2 = layers.Flatten()(at4)
a3 = layers.Flatten()(at5)
a4 = layers.Flatten()(at6)
at = layers.Concatenate()([a3, ang])

x = layers.Dense(128, activation="relu")(at)
x = layers.Dense(64, activation="relu")(x)
outputs = layers.Dense(20)(x)

#model = models.Sequential([
#        layers.Input(shape=(40, 40, 1)),
#        layers.Conv2D(32, (3, 3), activation='relu'),
#        layers.MaxPooling2D((2, 2)),
#        layers.Conv2D(64, (3, 3), activation='relu'),
#        layers.Flatten(),
#        layers.Dense(64, activation='relu'),
#        layers.Dense(20)
#    ])

model = Model([inputs, input2], outputs)

model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

model.summary()

#print(type(X_train))
#print(type(y_train))
#print(type(X_val))
#print(type(y_val))

history = model.fit([X_train, ang_train], y_train, epochs=5, validation_data=([X_val, ang_val], y_val))

test_loss, test_acc = model.evaluate([X_val, ang_val], y_val, verbose=2)


print('\nTest accuracy:', test_acc)
print('\nTest loss:', test_loss)
outs = model.predict([X_val, ang_val])


with open("output.txt", "w") as f:
  f.seek(0)
  for i in range(len(outs)):
    f.write(f"Output: {np.argmax(outs[i])} Real: {y_val[i]}\n")


model.save("model.keras")
#del model
# Recreate the exact same model purely from the file:
#model = keras.models.load_model("model.keras")


""" # how to do non sequential models
encoder_input = keras.Input(shape=(28, 28, 1), name="original_img")
x = layers.Conv2D(16, 3, activation="relu")(encoder_input)
x = layers.Conv2D(32, 3, activation="relu")(x)
x = layers.MaxPooling2D(3)(x)
x = layers.Conv2D(32, 3, activation="relu")(x)
x = layers.Conv2D(16, 3, activation="relu")(x)
"""
