data = "hi"

if  data = "hi":
    # Nifty is below 90-day moving average, send a push notification
    title = "Nifty Alert"
    message = "Nifty has closed below the 90-day moving average."
    if pb.push_note(title, message):
        print("Push notification sent successfully!")
    else:
        print("Push notification not sent!")
else:
    print("Nifty is not present in the output")