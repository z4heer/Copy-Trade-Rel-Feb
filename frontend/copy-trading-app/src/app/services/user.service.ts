import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private baseUrl = 'http://127.0.0.1:5000/api';

  constructor(private http: HttpClient) {}

  getAllUsers(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/all_users`)
      .pipe(
        catchError(this.handleError)
      );
  }

  addUser(userDetails: any): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/add_user`, userDetails)
      .pipe(
        catchError(this.handleError)
      );
  }

  modifyUser(userDetails: any): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/modify_user`, userDetails)
      .pipe(
        catchError(this.handleError)
      );
  }

  deleteUser(userid: string): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/delete_user`, { userid })
      .pipe(
        catchError(this.handleError)
      );
  }

  validateUser(userid: string): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/validate_user`, { userid })
      .pipe(
        catchError(this.handleError)
      );
  }

  private handleError(error: any): Observable<never> {
    // Handle error here
    console.error('An error occurred:', error);
    return throwError(error);
  }
}