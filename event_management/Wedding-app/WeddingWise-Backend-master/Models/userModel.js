import mongoose from "mongoose";

const userSchema = new mongoose.Schema(
  {
    username: {
      type: String,
      required: true,
      unique: true,
    },
    email: {
      type: String,
      required: true,
      unique: true,
    },
    password: {
      type: String,
      required: true,
    },
    profilePicture: {
      type: String,
      default: "https://static.vecteezy.com/system/resources/thumbnails/005/544/718/small_2x/profile-icon-design-free-vector.jpg"
    }
  },
  { timestamps: true }
);

const eventSchema = new mongoose.Schema(
  {
    name: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: true
    },
    date: {
      type: Date,
      required: true
    },
    userId: {
      type: [{ type: mongoose.Schema.Types.ObjectId, ref: 'User' }],
    }
  },
  { timestamps: true }

)

const User = mongoose.model("User", userSchema);
const Event = mongoose.model("Event", eventSchema);
export default User;