import React, { useState, useEffect, useRef } from "react";
import PropTypes from "prop-types";



// The parameter of this function is an object with a string called url inside it.
export default function Room({url}) {
  /* Display image and post owner of a single post */

    const [imgUrl, setImgUrl] = useState("");

    useEffect(() => {
    // Declare a boolean flag that we can use to cancel the API request.
    let ignoreStaleRequest = false;

    // Call REST API to get the post's information
    fetch(url, { credentials: "same-origin" })
        .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
        })
        .then((data) => {
        // If ignoreStaleRequest was set to true, we want to ignore the results of the
        // the request. Otherwise, update the state to trigger a new render.
        if (!ignoreStaleRequest) {
        }
        })
        .catch((error) => console.log(error));

    return () => {
        // This is a cleanup function that runs whenever the Post component
        // unmounts or re-renders. If a Post is about to unmount or re-render, we
        // should avoid updating state.
        ignoreStaleRequest = true;
    };
    }, [url]);

  // Render post image and post owner
    return ();
}

Post.propTypes = {};
