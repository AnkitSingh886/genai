import { Injectable } from '@angular/core';
    import { HttpClient } from '@angular/common/http';
    import { Observable } from 'rxjs';

    @Injectable({
        providedIn: 'root'
    })
    export class ApiService {
        constructor(private http: HttpClient) {}
    
        api_dashboard(): Observable<any> {
            return this.http.get('/api/dashboard');
        }
    
        api_lms_leave_apply(data: any): Observable<any> {
            return this.http.post('/api/lms/leave/apply', data);
        }
    
        api_lms_leave_approve(data: any): Observable<any> {
            return this.http.post('/api/lms/leave/approve', data);
        }
    
        api_pods_details(): Observable<any> {
            return this.http.get('/api/pods/details');
        }
    
        api_pods_recommend(data: any): Observable<any> {
            return this.http.post('/api/pods/recommend', data);
        }
    }
