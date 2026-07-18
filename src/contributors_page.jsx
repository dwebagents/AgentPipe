import React, { useEffect, useState } from'react';
import axios from 'axios';

const ContributorsPage = () => {
  const [contributors, setContributors] = useState([]);
  const [goldenEggs, setGoldenEggs] = useState([]);

  useEffect(() => {
    const fetchContributors = async () => {
      try {
        const response = await axios.get('https://api.github.com/repos/AgentPipe/repo-name/pulls');
        const uniqueContributors = [...new Set(response.data.map(pr => pr.user.login))];
        const contributorsData = uniqueContributors.map(login => ({
          login,
          html_url: `https://github.com/${login}`,
          avatar_url: `https://api.github.com/users/${login}`,
        }));
        setContributors(contributorsData);
      } catch (error) {
        console.error('Error fetching contributors:', error);
      }
    };

    const fetchGoldenEggs = async () => {
      try {
        const response = await axios.get('https://api.yourdomain.com/golden-eggs');
        setGoldenEggs(response.data);
      } catch (error) {
        console.error('Error fetching golden eggs:', error);
      }
    };

    fetchContributors();
    fetchGoldenEggs();
  }, []);

  return (
    <div className="contributors-page">
      <header className="hero">
        <img src="https://yourdomain.com/corporate-goose-factory.jpg" alt="Goose people working in a factory" />
      </header>
      <main>
        {contributors.map((contributor, index) => (
          <section key={index} className="contributor-section">
            <h2>{contributor.login}</h2>
            <img src={`https://yourdomain.com/goose-portraits/${contributor.login}.jpg`} alt={`${contributor.login} portrait`} />
            <p>Recent Prompt: <em>Dynamic data here</em></p>
            <a href={contributor.html_url} target="_blank" rel="noopener noreferrer">GitHub Profile</a>
          </section>
        ))}
        {goldenEggs.map((egg, index) => (
          <img key={index} src={egg.url} alt="Golden Egg" className="golden-egg" />
        ))}
        <div className="easter-egg-game">
          <h3>Find the hidden goose!</h3>
          <img src="https://yourdomain.com/hidden-goose.jpg" alt="Hidden Goose" />
        </div>
        <div className="number-71">
          {[...Array(71)].map((_, index) => (
            <span key={index}>71</span>
          ))}
        </div>
      </main>
      <footer>
        <p>Contact Information: C-Suite of AgentPipe</p>
        <video src="https://yourdomain.com/c-suite-waving.mp4" controls />
      </footer>
    </div>
  );
};

export default ContributorsPage;