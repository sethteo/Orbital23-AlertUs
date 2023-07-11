import React from 'react';
import {Link} from 'react-router-dom'

function Nav() {
    return (
        <nav class="navbar navbar-expand-lg bg-body-tertiary">
            <div class="container-fluid">
                <a class="navbar-brand" href="#">Navbar</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                    <div class="navbar-nav">
                        <Link to='/' className="nav-item nav-link active">Home</Link>
                        <Link to='/tweets' className="nav-item nav-link">Items</Link>
                    </div>
                </div>
            </div>
        </nav>
    )
}

export default Nav;