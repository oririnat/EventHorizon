import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { EventsWindowsComponent } from './events-windows/events-windows.component';
import { RecentElementsWindowsComponent } from './recent-elements-windows/recent-elements-windows.component';

@NgModule({
  declarations: [
    AppComponent,
    EventsWindowsComponent,
    RecentElementsWindowsComponent
  ],
  imports: [
    BrowserModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
