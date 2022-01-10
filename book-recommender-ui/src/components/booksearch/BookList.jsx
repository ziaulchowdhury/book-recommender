import * as React from 'react';

import Alert from '@mui/material/Alert';
import AlertTitle from '@mui/material/AlertTitle';

import { styled } from '@mui/material/styles';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardMedia from '@mui/material/CardMedia';

import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';

import { Link } from "react-router-dom";

export default function BookList(props) {

const Item = styled(Paper)(({ theme }) => ({
    ...theme.typography.body2,
    padding: theme.spacing(2),
    textAlign: 'center',
    color: theme.palette.text.secondary,
}));
    
  return (
    <>
        <Box sx={{ flexGrow: 1, pt: 5 }}>
            <Grid container spacing={3} sx={{ pl: 5, pr: 5 }}>
                {props.items.map(item => (
                    <Grid item xs={2} key={item.book_id}>
                        <Link to={{ pathname:`/book/${item.book_id}`, id: `${item.index}` }}>
                            <Card sx={{ minHeight: 250 }}>
                                <CardHeader subheader={item.title} minHeight="200"/>
                                <CardMedia
                                    component="img"
                                    width="98"
                                    minHeight="160"
                                    image={item.image_url}
                                />
                            </Card>
                        </Link>
                    </Grid>
                ))}
            </Grid>
        </Box>
        {props.emptyResult === true &&
            <Alert severity="info" width="100">
                <AlertTitle>Info</AlertTitle>
                Could not find any book for the given term!
            </Alert>
        }
    </>
  );
}
