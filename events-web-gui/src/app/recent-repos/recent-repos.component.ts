import { Component, OnInit } from '@angular/core';
import { RepositorySchema } from '../models';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-recent-repos',
  templateUrl: './recent-repos.component.html',
  styleUrls: ['./recent-repos.component.css']
})
export class RecentReposComponent implements OnInit {
  recent_repos: RepositorySchema[] = [];

  constructor() {
    console.log('RecentReposComponent constructor called');
  }

  ngOnInit() {
    console.log('RecentReposComponent ngOnInit called');

    this.loadRecentRepos();

    // run the loadRecentRepos function every 5 seconds
    setInterval(() => {
      this.loadRecentRepos();
    }, 5000);

  }

  loadRecentRepos() {
    // Fetch the recent repositories, /repositories with the parameter limit and skip
    fetch(`${environment.backendBaseUrl}/repositories/recent`)
      .then(response => response.json())
      .then(data => {
        console.log('Recent repositories:', data);

        // sort the repositories for consistency
        data.sort((a: RepositorySchema, b: RepositorySchema) => {
          return a.id - b.id;
        });
        this.recent_repos = data;
      })
      .catch(error => {
        console.log('Error fetching recent repositories:', error);
      });
  }
}
