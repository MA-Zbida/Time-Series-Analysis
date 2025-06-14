import tensorflow as tf
from keras.saving import register_keras_serializable

@register_keras_serializable(package='my_losses')
# Custom loss function that ignores padded values
def masked_mse_loss(mask_value=0.0):
    def loss(y_true, y_pred):
        # Create a mask for non-padded values (1 for real values, 0 for padded)
        mask = tf.cast(tf.not_equal(y_true, mask_value), tf.float32)
        
        # Calculate squared error
        squared_error = tf.square(y_true - y_pred)
        
        # Apply mask to squared error
        masked_squared_error = squared_error * mask
        
        # Sum the masked squared error and divide by the sum of the mask
        # (which gives us the count of non-padded values)
        mask_sum = tf.reduce_sum(mask, axis=-1)
        
        # Avoid division by zero
        mask_sum = tf.maximum(mask_sum, 1.0)
        
        return tf.reduce_sum(masked_squared_error, axis=-1) / mask_sum
    
    return loss

@register_keras_serializable(package="Custom")
def sum_pooling(x):
    return tf.reduce_sum(x, axis=1)