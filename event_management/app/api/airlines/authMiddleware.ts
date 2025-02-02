import { NextApiRequest, NextApiResponse, NextApiHandler } from 'next';

export function withAuth(handler: NextApiHandler) {
  return async (req: NextApiRequest, res: NextApiResponse) => {
    const token = req.headers.authorization;

    if (!token) {
      return res.status(401).json({ error: 'Unauthorized: No token provided' });
    }

    try {
      return await handler(req, res);
    } catch (error) {
      return res.status(403).json({ error: 'Forbidden: Invalid token' });
    }
  };
}

// eg
// import { withAuth } from '../../middleware/authMiddleware';
// export default withAuth(async function handler(req, res) {
//   res.status(200).json({ message: 'Authenticated request successful' });
// });