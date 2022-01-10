import { createSlice } from '@reduxjs/toolkit';

const searchSlice = createSlice({
  name: 'search',
  initialState: {
    items: [],
    searchTerm: 'gone wild',
    emptyResult: true,
    error: '',
  },
  reducers: {
    replaceSearchResults(state, action) {
      state.searchTerm = action.payload.searchTerm;
      state.items = action.payload.items;
      state.emptyResult = action.payload.emptyResult;
      state.error = action.payload.error;
    },
  },
});

export const searchActions = searchSlice.actions;

export default searchSlice;