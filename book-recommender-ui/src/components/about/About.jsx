import React, { Fragment } from 'react';
import classes from './About.module.css';

import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import { CardActionArea } from '@mui/material';
import Box from '@mui/material/Box';

const About = (props) => {
  return (
    <>
      <div className={classes.about}>
        <Typography gutterBottom variant="h5" component="div" style={{flexDirection: 'row', flex: 1}}>
          Web application for Book Recommendation! 
        </Typography>
        <Divider variant="middle" />
        <Typography gutterBottom variant="h7" component="div" style={{flexDirection: 'row', flex: 1}}>
          Recommendation system based on rating, number on recommendations and content based 
          recommendations for a better gift selection and popularisation the habit of reading.
        </Typography>
        <Typography gutterBottom variant="h7" component="div" style={{flexDirection: 'row', flex: 1}}>
          The application is developed by:
        </Typography>
      </div>

      <Box sx={{ flexGrow: 1, pt: 5 }}>
        <Grid container spacing={3} sx={{ pl: 5, pr: 5 }} alignItems="center" justifyContent="center">
            <Card sx={{ width: 500 }}>
              <CardActionArea>
                <CardMedia
                  component="img"
                  image="https://www.clipartmax.com/png/full/323-3235554_male-user-icon-icon-search-engine-male-user-icon.png"
                  alt="Ziaul"
                />
                <CardContent>
                  <Typography gutterBottom variant="h5" component="div">
                    Ziaul Islam Chowdhury
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    ziacho-9@student.ltu.se<br/>
                    School of Computer Science and Media technology<br/>
                    Linnaeus University, Växjö, Sweden
                  </Typography>
                </CardContent>
              </CardActionArea>
            </Card>
            <Card sx={{ width: 500, marginLeft: 2 }}>
              <CardActionArea>
                <CardMedia
                  component="img"
                  image="https://www.clipartmax.com/png/full/103-1038880_user-rubber-stamp-female-user-icon.png"
                  alt="green iguana"
                />
                <CardContent>
                  <Typography gutterBottom variant="h5" component="div">
                    Yuliya Vatsova
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    yv222am@student.lnu.se<br/>
                    School of Computer Science and Media technology<br/>
                    Linnaeus University, Växjö, Sweden
                  </Typography>
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>
      </Box>
    </> 
  );
};

export default About;