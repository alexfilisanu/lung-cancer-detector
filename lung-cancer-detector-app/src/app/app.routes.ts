import { Routes } from '@angular/router';
import { AboutComponent } from "./about/about.component";
import { DashboardComponent } from "./dashboard/dashboard.component";
import { AdminLayoutComponent } from "./admin-layout/admin-layout.component";
import { ContactUsComponent } from "./contact-us/contact-us.component";
import { CTPredictionComponent } from "./CT-prediction/CT-prediction.component";
import { WelcomeComponent } from "./welcome/welcome.component";
import { NotFoundComponent } from "./not-found/not-found.component";
import { AdvicesComponent } from "./advices/advices.component";
import { SurveyPredictionComponent } from "./survey-prediction/survey-prediction.component";
import { LoginComponent } from "./login/login.component";
import { RegisterComponent } from "./register/register.component";
import { AccountComponent } from "./account/account.component";

export const routes: Routes = [
  {
    path: '',
    component: WelcomeComponent
  },
  {
    path: 'login',
    component: LoginComponent
  },
  {
    path: 'register',
    component: RegisterComponent
  },
  {
    path: '',
    component: AdminLayoutComponent,
    children: [
      {
        path: 'dashboard',
        component: DashboardComponent
      },
      {
        path: 'CT-prediction',
        component: CTPredictionComponent
      },
      {
        path: 'survey-prediction',
        component: SurveyPredictionComponent
      },
      {
        path: 'about',
        component: AboutComponent
      },
      {
        path: 'advices',
        component: AdvicesComponent
      },
      {
        path: 'contact-us',
        component: ContactUsComponent
      },
      {
        path: 'account',
        component: AccountComponent
      }
    ]
  },
  {
    path: '**',
    component: NotFoundComponent
  }
];
