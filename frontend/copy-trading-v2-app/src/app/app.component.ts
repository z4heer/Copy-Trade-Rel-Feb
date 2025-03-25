import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { HeaderComponent } from './components/header/header.component';
import { NavigationComponent } from './components/navigation/navigation.component';
import { ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['../styles.css'],
  standalone: true,
  imports: [
    RouterModule,
    HeaderComponent,
    NavigationComponent,
    ReactiveFormsModule
  ]
})
export class AppComponent {}