import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from 'react-redux';

import Alert from '@mui/material/Alert';
import AlertTitle from '@mui/material/AlertTitle';

import BookList from "./BookList";
import useInput from './../../hooks/use-input';
import classes from './BookSearch.module.css';
// import { searchActions } from '../../store/search-slice';
// import { searchBooks } from '../../store/search-actions';

const isNotEmpty = (value) => value.trim() !== '';

const BookSearch = (props) => {

  const [items, setItems] = useState([]);
  const [error, setError] = useState(null);
  const [emptyResult, setEmptyResult] = useState(false);

  // const searchTermValue1 = useSelector((state) => state.search.searchTerm);

  const {
    value: searchTermValue,
    isValid: searchTermIsValid,
    hasError: searchTermHasError,
    valueChangeHandler: searchTermChangeHandler,
    inputBlurHandler: searchTermBlurHandler,
    reset: resetSearchTerm,
  } = useInput(isNotEmpty);

  let formIsValid = false;

  if (searchTermIsValid) {
    formIsValid = true;
  }

  /*
  const dispatch = useDispatch();
  useEffect(() => {
    dispatch(searchBooks(searchTermValue));
  }, [searchTermValue, dispatch]);
  */

  const submitHandler = async(event) => {
    event.preventDefault();
    if (!formIsValid) {
      return;
    }

    try {
      const response = await fetch('http://localhost:8080/book/search?' + new URLSearchParams({ title: searchTermValue }), {
        method: 'GET'
      });
      const data = await response.json();
      setItems(data.data);
      setEmptyResult(data.data.length === 0);
    } catch (error) {
      setError(error);
    }
    // resetSearchTerm();

    /*
    dispatch(
      searchActions.replaceSearchResults({
        searchTerm: searchTermValue
      })
    ).then(() => {
      dispatch(searchBooks(searchTermValue));
   });
   */
  };

  // const bookItems = useSelector((state) => state.search.items);
  // searchTermValue = useSelector((state) => state.search.searchTerm);
  // const errorValue = useSelector((state) => state.search.error);
  // const emptyResultValue = useSelector((state) => state.search.emptyResult);

  /* dispatch(AddBilling.action(formData)).then(() => {} */

  const searchTermClasses = searchTermHasError ? 'form-control invalid' : 'form-control';
  
  return (
    <>
      <form onSubmit={submitHandler}>
        <div className='control-group' className={classes['book-search']}>
          <div className={searchTermClasses}> 
            <input
              type='text'
              id='search-term'
              value={searchTermValue}
              onChange={searchTermChangeHandler}
              onBlur={searchTermBlurHandler}
              className={classes['large-input']}
            />
            <button disabled={!formIsValid} className={classes['large-button']}>Search</button>
            {searchTermHasError && <p className="error-text">Please enter search term</p>}
          </div>
        </div>
      </form>

      {error && 
        <Alert severity="error" width="100">
            <AlertTitle>Error</AlertTitle>
            {error.message}
        </Alert>
      }

      <BookList items={items}  emptyResult={emptyResult} /> 
      { /* <BookList items={bookItems}  emptyResult={emptyResultValue} /> */ }
    </>
  );
};

export default BookSearch;
