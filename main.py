import cv2
import mediapipe as mp
import serial #Import Necessary Modules

#Initialize Serial connection and HandTracking Module
com = "COM4"
baud = 9600
ser = serial.Serial(com, baud, timeout=0.1)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
cap = cv2.VideoCapture(0)

#Function for mapping hand reading to servo
def map_range(value, in_min=0, in_max=640, out_min=0, out_max=180):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

#Infinite main loop
while True:
    success, frame = cap.read() #Initialize the frame (webcam)
    if not success:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb) #Convert BGR into RGB color format for manipulation

    if result.multi_hand_landmarks: #Check for hand landmarks
        for hand in result.multi_hand_landmarks:
            lm = hand.landmark[9]
            h, w, _ = frame.shape
            cx, cy = int(lm.x * w), int(lm.y * h) #Get coordinates; track hand in realtime

            # Draw + Print coordinates
            cv2.circle(frame, (cx, cy), 10, (255, 0 , 0), cv2.FILLED)

            ServoRotateReading = round(map_range(cx),1) #Collect coordinate readings for arduino output
            ServoArmReading = "STOP"

            if cy <= 85: #Threshold zones for arm servo
                ServoArmReading = "UP"
            elif cy >= 420:
                ServoArmReading = "DOWN"
            else:
                ServoArmReading = "STOP"
            print (f"Rotation: {ServoRotateReading}. Arm: {ServoArmReading}") #Output in python for debugging
            output_phrase = (f"{ServoRotateReading},{ServoArmReading}\n") #Generate output phrase to send all at once to arduino
            ser.write(output_phrase.encode("utf-8")) #Send to arduino

    cv2.rectangle(frame, (0, 0), (640, 85), (0, 255, 0), 5) #Draw bounds for up and down controls for visual aid
    cv2.rectangle(frame, (0,420), (640, 500), (0,0, 255), 5)
    cv2.imshow("Palm Tracker", frame) #Show the frame to the user to watch in realtime

    if cv2.waitKey(1) & 0xFF == ord('q'): #Exiting the loop
        break

cap.release()
cv2.destroyAllWindows() #Release the capture and close the window
