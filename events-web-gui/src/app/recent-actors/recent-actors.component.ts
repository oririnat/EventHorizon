import { Component, OnInit } from '@angular/core';
import { ActorSchema } from '../models';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-recent-actors',
  templateUrl: './recent-actors.component.html',
  styleUrls: ['./recent-actors.component.css']
})
export class RecentActorsComponent implements OnInit {
  recent_actors: ActorSchema[] = [];

  constructor() {
    console.log('RecentActorsComponent constructor called');
  }

  ngOnInit() {
    console.log('RecentActorsComponent ngOnInit called');

    // Fetch the recent actors, /actors with the parameter limit and skip
    fetch(`${environment.backendBaseUrl}/actors/recent`)
      .then(response => response.json())
      .then(data => {
        console.log('Recent actors:', data);
        this.recent_actors = data;
      })
      .catch(error => {
        console.log('Error fetching recent actors:', error);
      });
  }

}
