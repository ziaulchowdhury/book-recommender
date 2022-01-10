import React, { Fragment } from 'react';

import { fontSize } from '@mui/system';
import { Link } from "react-router-dom";

import logo from '../../assets/logo.png';
import classes from './Header.module.css';

const Header = (props) => {
  return (
    <Fragment>
      <header className={classes.header}>
        <nav className={classes.linksStyle}>
          <Link to="/" ><img src={logo} className={classes['main-image']}/></Link>
          <Link to="/about"><span style={{fontSize: 20, paddingLeft: 5}}>About</span></Link>
        </nav>
      </header>
    </Fragment>
  );
};

export default Header;
