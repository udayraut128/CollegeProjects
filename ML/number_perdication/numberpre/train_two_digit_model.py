import numpy as np
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical


def create_two_digit_dataset(images, labels, num_samples=30000):
    data = []
    targets = []
    for _ in range(num_samples):
        idx1, idx2 = np.random.randint(0, len(images)), np.random.randint(0, len(images))
        img1, img2 = images[idx1], images[idx2]
        lbl1, lbl2 = labels[idx1], labels[idx2]
        combined_img = np.hstack((img1, img2))  # Side-by-side
        combined_label = lbl1 * 10 + lbl2
        data.append(combined_img)
        targets.append(combined_label)
    return np.array(data), np.array(targets)

print("Loading MNIST dataset...")
(x_train_single, y_train_single), (x_test_single, y_test_single) = mnist.load_data()

print("Creating training data...")
x_train, y_train = create_two_digit_dataset(x_train_single, y_train_single, 30000)
print("Creating testing data...")
x_test, y_test = create_two_digit_dataset(x_test_single, y_test_single, 5000)

# Reshape & normalize
x_train = x_train.reshape(-1, 28, 56, 1).astype("float32") / 255
x_test = x_test.reshape(-1, 28, 56, 1).astype("float32") / 255

# One-hot encode labels
y_train = to_categorical(y_train, 100)
y_test = to_categorical(y_test, 100)


model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(28,56,1)),
    MaxPooling2D(pool_size=(2,2)),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(pool_size=(2,2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(100, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


print("Training model...")
model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=5, batch_size=200)


model.save("two_digit_model.h5")
print("Model saved as two_digit_model.h5")

