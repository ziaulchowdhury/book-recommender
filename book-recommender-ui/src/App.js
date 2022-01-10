// import { Fragment, useState } from 'react';
import React, { Component, Fragment, useState }  from 'react';

import { Routes, Route, Link } from "react-router-dom";

import Layout from './components/Layout/Layout';
import BookSearch from './components/booksearch/BookSearch';
import About from './components/about/About';
import BookDetails from './components/booksearch/BookDetails'; 

import './App.css';

function App() {
  return (
    <Fragment>
      <Layout>
        <Routes>
          <Route path="/" element={<BookSearch />} />
          <Route path="about" element={<About />} />
          <Route path="/book/:bookId" element={<BookDetails />} />
        </Routes>
      </Layout>
    </Fragment>
  );
}

export default App;
