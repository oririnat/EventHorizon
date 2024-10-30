import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { EventsWindowsComponent } from './events-windows/events-windows.component';
import { RecentReposComponent } from './recent-repos/recent-repos.component';
import { RecentActorsComponent } from './recent-actors/recent-actors.component';

@NgModule({
  declarations: [
    AppComponent,
    EventsWindowsComponent,
    RecentReposComponent,
    RecentActorsComponent
  ],
  imports: [
    BrowserModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
