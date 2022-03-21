model = Sequential()
#first layer
model.add(Conv2D(32,(5,5), activation='relu', input_shape = (32,32,3)))
#pooling layer
model.add(MaxPooling2D(pool_size=(2,2)))
#add another convolution layer
model.add(Conv2D(32,(5,5), activation='relu'))
#add another pooling layer
model.add(MaxPooling2D(pool_size=(2,2)))
#add a flattening layer
model.add(Flatten())
#add a layer with 1000 neurons
model.add(Dense(1000, activation='relu'))
#add a dropout layer
model.add(Dropout(0.5))
#add a layer with 500 neurons
model.add(Dense(500, activation='relu'))
#add a dropout layer
model.add(Dropout(0.5))
#add a layer with 250 neurons
model.add(Dense(250, activation='relu'))
#add a layer with 10 neurons
model.add(Dense(10, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

#training the model
hist = model.fit(x_train, y_train_one_hot, batch_size=256, epochs=10, validation_split=0.2)
#25:56