import React, { Fragment, useState, useEffect } from 'react';
import { useParams, Route } from 'react-router-dom';

import Alert from '@mui/material/Alert';
import AlertTitle from '@mui/material/AlertTitle';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardMedia from '@mui/material/CardMedia';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import PropTypes from 'prop-types';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import SearchIcon from '@mui/icons-material/Search';

import BookList from "./BookList";
import classes from './BookDetails.module.css';
import getLanguageName from '../../utils/Utils';

function TabPanel(props) {
    const { children, value, index, ...other } = props;
  
    return (
      <div
        role="tabpanel"
        hidden={value !== index}
        id={`simple-tabpanel-${index}`}
        aria-labelledby={`simple-tab-${index}`}
        {...other}
      >
        {value === index && (
          <Box sx={{ p: 3 }}>
            <Typography>{children}</Typography>
          </Box>
        )}
      </div>
    );
  }
  
  TabPanel.propTypes = {
    children: PropTypes.node,
    index: PropTypes.number.isRequired,
    value: PropTypes.number.isRequired,
  };
  
  function a11yProps(index) {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };
  }

const BookDetails = (props) => {

    const { bookId } = useParams();

    const [bookDetails, setBookDetails] = useState(null);
    const [error, setError] = useState(null);
    const [emptyResult, setEmptyResult] = useState(false);

    const [booksFromSameAuthors, setBooksFromSameAuthors] = useState([]);
    const [errorBooksFromSameAuthors, setErrorBooksFromSameAuthors] = useState(null);
    const [emptyResultBooksFromSameAuthors, setEmptyResultBooksFromSameAuthors] = useState(false);

    const [booksFromSimilarRating, setBooksFromSimilarRating] = useState([]);
    const [errorBooksFromSimilarRating, setErrorBooksFromSimilarRating] = useState(null);
    const [emptyResultBooksFromSimilarRating, setEmptyResultBooksFromSimilarRating] = useState(false);

    const [booksFromCollaFiltering, setBooksFromCollaFiltering] = useState([]);
    const [errorBooksFromCollaFiltering, setErrorBooksFromCollaFiltering] = useState(null);
    const [emptyResultBooksFromCollaFiltering, setEmptyResultBooksFromCollaFiltering] = useState(false);

    const [value, setValue] = React.useState(0);

    useEffect(() => {
        loadBookDetails();
    }, []);

    useEffect(() => {
        loadBooksFromSameAuthors();
    }, []);

    useEffect(() => {
        loadBooksFromSimilarRating();
    }, []);

    useEffect(() => {
        loadBooksFromCollaborativeRecommendation();
    }, []);

    const loadBookDetails = async() => {
        try {
            const response = await fetch('http://localhost:8080/book?' + new URLSearchParams({ book_id: bookId }), {
                method: 'GET'
            });
            const data = await response.json();
            // console.log('data: ', data);

            const containsResult = data.data.length === 1;
            if(containsResult) {
                setBookDetails(data.data[0]);
            }
            
            setEmptyResult(!containsResult);
        } catch (error) {
            setError(error);
        }
    };

    const loadBooksFromSameAuthors = async() => {
        try {
            const response = await fetch('http://localhost:8080/book/recommend/same_author?' + new URLSearchParams({ book_id: bookId }), {
                method: 'GET'
            });
            const data = await response.json();
            console.log('data: ', data);

            const containsResult = data.data? data.data.length > 0 : false;
            if(containsResult) {
                setBooksFromSameAuthors(data.data);
            }
            
            setEmptyResultBooksFromSameAuthors(data.data.length === 0);
        } catch (error) {
            setErrorBooksFromSameAuthors(error);
        }
    };

    const loadBooksFromSimilarRating = async() => {
        try {
            const response = await fetch('http://localhost:8080/book/recommend/similar_rating?' + new URLSearchParams({ book_id: bookId }), {
                method: 'GET'
            });
            const data = await response.json();
            console.log('data: ', data);

            const containsResult = data.data? data.data.length > 0 : false;
            if(containsResult) {
                setBooksFromSimilarRating(data.data);
            }
            
            setEmptyResultBooksFromSimilarRating(!containsResult);
        } catch (error) {
            setErrorBooksFromSimilarRating(error);
        }
    };
    
    const loadBooksFromCollaborativeRecommendation = async() => {
        try {
            const response = await fetch('http://localhost:8080/book/recommend/collaborative?' + new URLSearchParams({ book_id: bookId }), {
                method: 'GET'
            });
            const data = await response.json();
            console.log('data: ', data);

            const containsResult = data.data? data.data.length > 0 : false;
            if(containsResult) {
                setBooksFromCollaFiltering(data.data);
            }
            
            setEmptyResultBooksFromCollaFiltering(!containsResult);
        } catch (error) {
            setErrorBooksFromCollaFiltering(error);
        }
    };
    
    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    return (
        <div className={classes['book-details']}>
            {bookDetails && (
                <Box sx={{ flexGrow: 1, pt: 5 }}>
                    <Grid container spacing={3} sx={{ pl: 5, pr: 5 }}>
                        <Card sx={{ width: 350 }}>
                            <CardMedia
                                component="img"
                                width="98"
                                minHeight="160"
                                image={bookDetails.image_url}
                            />
                        </Card>
                        <Card>
                            <CardHeader title={bookDetails.original_title? bookDetails.original_title : bookDetails.title}/>
                            <CardHeader title="Author(s)" subheader={bookDetails.authors}/>
                            <CardHeader title="Language" subheader={getLanguageName(bookDetails.language_code)}/>
                            <CardHeader title="Average Rating" subheader={bookDetails.average_rating}/>
                            { /*<Slider size="small" defaultValue={bookDetails.average_rating}
                                step={1} marks min={0} max={5} disabled /> */ }
                            
                            <CardHeader title="Rated By" subheader={bookDetails.ratings_count}/>
                            <CardHeader title="Rating credebility" subheader={bookDetails.ratings_credebility.toFixed(4)}/>
                        </Card>
                        <Button variant="outlined" href="/" style={{marginLeft: 20}}>
                            <SearchIcon />
                            Back to Search
                        </Button>
                        
                    </Grid>
                </Box>
            )}
            {error && 
                <Alert severity="error" width="100">
                    <AlertTitle>Error</AlertTitle>
                    {error.message}
                </Alert>
            }
            {emptyResult === true &&
                <Alert severity="info" width="100">
                    <AlertTitle>Info</AlertTitle>
                    Could not find a book with index {bookId}!
                </Alert>
            }
            <Box sx={{ borderBottom: 1, borderColor: 'divider', pt: 5 }}>
                <Tabs value={value} onChange={handleChange} aria-label="basic tabs example">
                    <Tab label="By The Same Author(s)" {...a11yProps(0)} />
                    <Tab label="Similar Rating Books" {...a11yProps(1)} />
                    <Tab label="Recommended by Us" {...a11yProps(2)} />
                </Tabs>
            </Box>
            <TabPanel value={value} index={0}>
                {booksFromSameAuthors &&
                    <BookList items={booksFromSameAuthors}  emptyResult={emptyResultBooksFromSameAuthors} />
                }
            </TabPanel>
            <TabPanel value={value} index={1}>
                {booksFromSimilarRating &&
                    <BookList items={booksFromSimilarRating}  emptyResult={emptyResultBooksFromSimilarRating} />
                }
            </TabPanel>
            <TabPanel value={value} index={2}>
                {booksFromCollaFiltering &&
                    <BookList items={booksFromCollaFiltering}  emptyResult={emptyResultBooksFromCollaFiltering} />
                }
            </TabPanel>
            
        </div>
    );
};

export default BookDetails;
