import User from "../Models/userModel.js";
import { errorHandler } from "../Utils/Error.js";
import bcryptjs from "bcryptjs";
import jwt from "jsonwebtoken";
import dotenv from "dotenv";
dotenv.config();

export const registerUser = async (req, res, next) => {
  const { username, email, password } = req.body;
  if (
    !username ||
    !email ||
    !password ||
    username === "" ||
    email === "" ||
    password === ""
  ) {
    return next(errorHandler(400, "All the Fields Are Required"));
  }
  const hashedPassword = bcryptjs.hashSync(password, 10);

  const newUser = new User({ username, email, password: hashedPassword });
  try {
    await newUser.save();
    res
      .status(200)
      .json({ message: "User Registered Successfully", result: newUser });
  } catch (error) {
    res
      .status(200)
      .json({ message: "Error in User Registration" });
    next();
  }
};

export const loginUser = async (req, res, next) => {
  const { email, password } = req.body;
  if (!email || !password || email === "" || password === "") {
    return next(errorHandler(400, "All the Fields Are Required"));
  }
  try {
    const userDetail = await User.findOne({ email });
    const userPassword = bcryptjs.compareSync(password, userDetail.password);
    if (!userDetail || !userPassword) {
      return next(errorHandler(400, "Invalid Credentials"));
    }
    const token = jwt.sign(
      { id: userDetail._id, isAdmin: userDetail.isAdmin },
      process.env.JWT_SECRET_KEY
    );

    const { password: passkey, ...rest } = userDetail._doc;

    res
      .status(200)
      .json({ message: "User LoggedIn Successfully", rest, token });
  } catch (error) {
    res
      .status(200)
      .json({ message: "Error in User Login" });
    next();
  }
};



export const registerEvent = async (req, res, next) => {
  const {  date, userId } = req.body;
  if ( !date || !userId ||  date ==="" ) {
    return next(errorHandler(400, "All the Fields Are Required"));
  }
  try {
    const eventDetail = await Event.findOne({ name });
    if (eventDetail) {
      return next(errorHandler(400, "Event Already Exists"));
    }
    const newEvent = new Event({
      date,
      userId
    });
    await newEvent.save();
    res.status(200).json({ message: "Event Created Successfully" });
    next();
  }
  catch (error) {
    res.status(200).json({ message: "Error in Event Creation" });
    next();
  }
}