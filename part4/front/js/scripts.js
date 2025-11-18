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


/// Check user authentication
async function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementsByClassName('login-button');

    for (const link of loginLink) {
        link.style.display = token ? 'none' : 'block';
    }

    if (token) {
        // Fetch places data if the user is authenticated
        const places = await fetchPlaces(token);

        /// Populate places list
        place_list = document.getElementById('places-list');
        place_list.innerHTML = "";
        
        places.forEach(place => {
            const card = document.createElement('div');
            card.classList.add('place-card');
            card.innerHTML = `
                <h3>Name</h3>
                <p>${place.title}</p>
                <h3>Price</h3>
                <p data-price="${place.price}">${place.price}</p>
                <h3>Description</h3>
                <p>${place.description}</p>
                <h3>Position</h3>
                <p>${place.latitude} ${place.longitude}</p>
            `;
            place_list.appendChild(card);
        });
    }
}

window.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
});

document.getElementById('price-filter').addEventListener('change', (event) => {
    const selectedValue = event.target.value;

    const placeCards = document.querySelectorAll('.place-card');
    placeCards.forEach(card => {
        const price = parseFloat(card.querySelector('p[data-price]').dataset.price);

        if (selectedValue === 'All' || price <= parseFloat(selectedValue)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
});
