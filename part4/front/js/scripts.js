/// Request for login
async function loginUser(email, password) {
    const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });
    return response;
}


///Logout 
function logout() {
    document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    location.reload();
}
document.addEventListener("DOMContentLoaded", () => {
    const logoutBtn = document.getElementById("logout");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", logout);
    }
});

/// Try to login
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await loginUser(email, password);

                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `token=${data.access_token}; path=/`;
                    window.location.href = 'index.html';
                } else {
                    const errorData = await response.json();
                    alert('Login failed: ' + (errorData.error || response.statusText));
                }
            } catch (error) {
                console.error('Error during login:', error);
                alert('An error occurred. Please try again.');
            }
        });
    }
});

/// Fetch places data
async function fetchPlaces(token) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const places = await response.json();
    return places;
  } catch (error) {
    console.error("Error fetching places :", error);
    return [];
  }
}

/// Fetch the token in the cookie
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}


///Create user
async function postUser(first_name, last_name, email, password) {
    const response = await fetch('http://127.0.0.1:5000/api/v1/users/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({first_name, last_name, email, password })
    });
    return response
}

/// Check user authentication
async function checkHomeAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementsByClassName('login-button');
    const logout = document.getElementById('logout');

    for (const link of loginLink) {
        if (token) {
            link.style.display = 'none';
            logout.style.display = 'block';
        } else {
            link.style.display = 'block';
            logout.style.display = 'none';
        }
    }

    if (token) {
        // Fetch places data if the user is authenticated
        const places = await fetchPlaces(token);

        /// Populate places list
        const place_list = document.getElementById('places-list');
        place_list.innerHTML = "";
        
        places.forEach(place => {
            const card = document.createElement('div');
            card.classList.add('place-card');
            card.innerHTML = `
                <h3>Name</h3>
                <p>${place.title}</p>
                <h3>Price per night</h3>
                <p data-price="${place.price}">${place.price}</p>
                <h3>Position</h3>
                <p>${place.latitude} ${place.longitude}</p>

                <button onclick="window.location.href='place.html?id=${place.id}'">
                    See details
                </button>
            `;
            place_list.appendChild(card);
        });
    } else {
        price = document.querySelector('.places-wrapper');
        places = document.querySelector('.places-content');
        main = document.querySelector('main');
        price.style.display = 'none';
        places.style.display = 'none';

        const message = document.createElement('h1');
        message.classList.add('auth-message');
        message.textContent = 'Please log in to see the available places.';
        main.appendChild(message);
    }
}

/// Get the place id
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("id");
}

/// Fetch place detail
async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = {};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
            method: 'GET',
            headers
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error("Error fetching place :", error);
        return null;
    }
}

async function checkPlaceAuthentication() {
    const token = getCookie('token');
    const placeId = getPlaceIdFromURL();
    const addReviewSection = document.getElementById('add-review');

    if (!placeId) return;

    const loginLink = document.getElementsByClassName('login-button');
    const logout = document.getElementById('logout');

    for (const link of loginLink) {
        if (token) {
            link.style.display = 'none';
            logout.style.display = 'block';
        } else {
            link.style.display = 'block';
            logout.style.display = 'none';
        }
    }

    if (addReviewSection) {
        addReviewSection.style.display = token ? 'block' : 'none';
    }

    const place = await fetchPlaceDetails(token, placeId);
    if (!place) return;

    const placeInfo = document.querySelector('.place-info');
    placeInfo.innerHTML = `
        <h3>Name</h3><p>${place.title}</p>
        <h3>Price</h3><p>${place.price}</p>
        <h3>Description</h3><p>${place.description}</p>
        <h3>Latitude</h3><p>${place.latitude}</p>
        <h3>Longitude</h3><p>${place.longitude}</p>
        <h3>Amenities</h3>
            <ul>
                ${place.amenities.map(amenity => `<li>${amenity.name}</li>`).join('')}
            </ul>
    `;

    const reviewsCard = document.querySelector('.review-card')
    reviewsCard.innerHTML = '';
    place.reviews.forEach(review => {
    const card = document.createElement('div');
    card.classList.add('review-item');
    card.innerHTML = `
        <h4>${review.name}</h4>
        <p>Rating: ${review.rating} / 5</p>
        <p>${review.text}</p>
    `;
    console.log(review);
    reviewsCard.appendChild(card);});
    console.log(place.reviews);
    const addReviewButton = document.createElement('button');
    addReviewButton.textContent = 'Add Review';
    addReviewButton.addEventListener('click', () => {
        window.location.href = `add_review.html?id=${place.id}`;
    });
    placeInfo.appendChild(addReviewButton);
}


/// Post Review
async function submitReview(token, placeId, text, rating) {
    const response = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
        method : 'POST',
        headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
        body: JSON.stringify({
            place_id: placeId,
            text: text,
            rating: rating
        })
    });
        return response;
}

function checkReviewsAuthentication() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'index.html';
    }
    return token;
}



document.addEventListener('DOMContentLoaded', () => {
    const placeList = document.getElementById('places-list');
    if (placeList) {
        checkHomeAuthentication();
    }

    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            const selectedValue = event.target.value;
            const placeCards = document.querySelectorAll('.place-card');
            placeCards.forEach(card => {
                const price = parseFloat(card.querySelector('p[data-price]').dataset.price);
                card.style.display = selectedValue === 'All' || price <= parseFloat(selectedValue) ? 'block' : 'none';
            });
        });
    }

    const placeInfo = document.querySelector('.place-info');
    if (placeInfo) {
        checkPlaceAuthentication();
    }

    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        const token = checkReviewsAuthentication();
        const placeId = getPlaceIdFromURL();
        const loginLink = document.getElementsByClassName('login-button');

        for (const link of loginLink) {
            link.style.display = token ? 'none' : 'block';
        }
        
        const buttonReview = document.getElementById('button_review');
        buttonReview.addEventListener('click', async () => {
            const text = document.getElementById('review').value;
            const rating = document.getElementById('rating').value;
            try {
                const response = await submitReview(token, placeId, text, rating);

                if (response.ok) {
                    window.location.href = `http://127.0.0.1:5500/part4/front/place.html?id=${placeId}`;
                    alert('Review submitted successfully!');
                } else {
                    const errorData = await response.json();
                    alert('Failed to submit review: ' + (errorData.error || response.statusText));
                }
            } catch (error) {
                console.error('Error during posting review:', error);
                alert('An error occurred. Please try again.');
            }
        });
    }


    const createUser = document.getElementById('create_user');
    if (createUser) {
        const buttonUser = document.getElementById('create_user_button')
        buttonUser.addEventListener('click', async () => {

            const first_name = document.getElementById('first_name').value;
            const last_name = document.getElementById('last_name').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await postUser(first_name, last_name, email, password);

                if (response.ok) {
                    window.location.href = 'login.html';
                } else {
                    const errorData = await response.json();
                    alert('Login failed: ' + (errorData.error || response.statusText));
                }
            } catch (error) {
                console.error('Error during account creation:', error);
                alert('An error occurred. Please try again.');
            }
        });    
    }
});