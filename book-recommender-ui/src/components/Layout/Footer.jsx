import React, { Fragment } from 'react';
import classes from './Footer.module.css';

const Footer = (props) => {
  return (
      <>
    <div style={{
        backgroundImage: `url(${require('../../assets/footer-image.png')})`,
        backgroundRepeat: 'repeat-x',
        width: '100%',
        height: 100,
        marginTop: 50
      }}>
    </div>
    </>
  );
};

export default Footer;
