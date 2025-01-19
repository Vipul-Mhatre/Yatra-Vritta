const jwt = require('jsonwebtoken');

const authMiddleware = (Models) => {
    // console.log(Models);
    return async (req, res, next) => {
        const token = req.header('Authorization');
        // console.log(token);
        // console.log("Request Headers: ", req.headers);

        if (!token) {
            return res.status(401).json({ message: "Unauthorized: Token not provided" });
        }

        const jwtToken = token.replace(/^Bearer\s/, "").trim();
        // console.log("Token from middleware ", jwtToken);

        try {
            const isVerified = jwt.verify(jwtToken, process.env.JWT_SECRET_KEY);
            console.log("Decoded Token: ", isVerified);

            // Loop through Models to check which model to use
            let userData = null;
            for (let Model of Models) {
                userData = await Model.findById(isVerified._id).select({ password: 0 });
                if (userData) break;
            }

            console.log("UserData: ", userData);

            if (!userData) {
                console.log("User or Organization not found");
                return res.status(401).json({ message: "User or Organization not found" });
            }

            req.user = userData;
            req.token = token;
            req.userID = userData._id;

            next();
        } catch (error) {
            console.log(error);
            return res.status(500).json({ message: "Internal Server Error" });
        }
    };
};



module.exports = authMiddleware;