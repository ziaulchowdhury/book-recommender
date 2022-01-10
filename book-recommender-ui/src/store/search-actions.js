import { searchActions } from './search-slice';

export const searchBooks = (searchTerm) => {

  return async (dispatch) => {

    const fetchData = async () => {
      console.log('HERE ................. fetchData ');

      const response = await fetch('http://localhost:8080/book/search?' + new URLSearchParams({ title: searchTerm }), {
        method: 'GET'
      });

      if (!response.ok) {
        throw new Error('Could not search books!');
      }

      const data = await response.json();
      return data;
    };

    try {
      const searchResults = await fetchData();
      dispatch(
        searchActions.replaceSearchResults({
          items: searchResults.data || [],
          searchTerm: searchTerm,
          emptyResult: searchResults.data? true : searchResults.data.length === 0,
          error: null, 
        })
      );
    } catch (error) {
      searchActions.replaceSearchResults({
        error: error, 
      })
    }
  };
};
