document.write(`
<nav>
  <div class="logo">
    <img src="https://res.cloudinary.com/dm4vmfqle/image/upload/v1745707988/1000_F_268887497_zUduupxYhFf0plFgjgga03unIi8ovX0k-removebg-preview_1_vhe8zr.png" alt="Logo">
  </div>

  <div class="nav-links">
    <a href='index.html'>Home</a>
    <a href="#services">Services</a>
    <a href="#contact">Contact</a>
    <a href='chat.html'target="_blank">Chat Now</a>
  </div>

  <div class="signup-btn">
    <button>Sign Up</button>
  </div>
</nav>

<style>
  nav {
    background-color: #F7F7F7;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.5rem 1.5rem;
    border-radius: 30px;
    width: 75%;
    max-width: 1200px;
    margin: 1rem auto;
    position: fixed;
    top: -4px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 1000;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    height: 45px;
  }

  .logo {
    flex: 1;
  }

  .logo img {
    height: 66px;
    width: auto;
  }

  .nav-links {
    flex: 2;
    display: flex;
    justify-content: center;
    gap: 2rem;
    align-items: center;
  }

  .nav-links a {
    text-decoration: none;
    color: #333;
    font-weight: 500;
    transition: color 0.3s;
  }

  .nav-links a:hover {
    color: #2B7A69;
  }

  .signup-btn {
    flex: 1;
    display: flex;
    justify-content: flex-end;
  }

  .signup-btn button {
    background-color: #2B7A69;
    color: white;
    padding: 0.6rem 1.2rem;
    border: none;
    border-radius: 20px;
    font-weight: bold;
    cursor: pointer;
    transition: background 0.3s;
    font-size: 0.95rem;
  }

  .signup-btn button:hover {
    background-color: #24695b;
  }
</style>
`);