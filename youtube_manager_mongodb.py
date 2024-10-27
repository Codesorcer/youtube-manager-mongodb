from pymongo import MongoClient
from dotenv import dotenv_values
from bson import ObjectId

config = dotenv_values(".env")

client = MongoClient(config["MONGOURL"], tlsAllowInvalidCertificates=True)

# Check if connection to MongoDB is successful
try:
    client.admin.command('ping')
    print("MongoDB connected successfully.")
except Exception as e:
    print("Could not connect to MongoDB:", e)

db = client["ytmanager"]
video_collection = db["videos"]

print(video_collection)

def list_videos():
    for video in video_collection.find():
        print(f"ID: {video['_id']}, Name: {video.get('name', 'N/A')} and Time: {video.get('time', 'N/A')}")

def add_video(name, time):
    video_collection.insert_one({"name": name, "time": time})

def update_video(video_id, new_name, new_time):
    # Convert video_id to ObjectId
    try:
        video_collection.update_one({'_id': ObjectId(video_id)}, {"$set": {"name": new_name, "time": new_time}})
    except Exception as e:
        print("Error updating video:", e)

def delete_video(video_id):
    # Convert video_id to ObjectId
    try:
        video_collection.delete_one({"_id": ObjectId(video_id)})
    except Exception as e:
        print("Error deleting video:", e)

def main():
    while True:
        print("\n Youtube Manager App")
        print("1. List all videos")
        print("2. Add a new video")
        print("3. Update a video")
        print("4. Delete a video")
        print("5. Exit the app")
        choice = input("Enter your choice: ")

        if choice == '1':
            list_videos()
        elif choice == '2':
            name = input("Enter the video name: ")
            time = input("Enter the video time: ")
            add_video(name, time)
        elif choice == '3':
            video_id = input("Enter the video id to update: ")
            name = input("Enter the updated video name: ")
            time = input("Enter the video time: ")
            update_video(video_id, name, time)
        elif choice == '4':
            video_id = input("Enter the video id to delete: ")
            delete_video(video_id)
        elif choice == '5':
            break
        else:
            print("Invalid Choice")

if __name__ == "__main__":
    main()
