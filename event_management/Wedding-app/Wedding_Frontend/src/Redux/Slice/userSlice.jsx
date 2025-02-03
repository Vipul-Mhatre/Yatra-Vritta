import { createSlice } from '@reduxjs/toolkit';

const initialState = {
    currentuser: null,
  loading: false,
  error: null
  
};

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    signInStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    signInSuccess: (state, action) => {
        state.currentuser = action.payload;
      state.loading = false;
      state.user = action.payload;
    },
    signInFailure: (state, action) => {
      state.loading = false;
      state.error = action.payload;
    },
    signOutSuccess: (state) => {
        state.currentuser = null;
        state.loading = false;
        state.error = null;
      },
  },
});

export const { signInStart, signInSuccess, signInFailure ,signOutSuccess } = userSlice.actions;
export default userSlice.reducer;
