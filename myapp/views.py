from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from myapp.forms import InfoForm, WorkoutForm, QuickInsertForm, DayForm
from myapp.models import workout, info, day
from django.urls import reverse
from datetime import date
from datetime import datetime
import re
from django.db.models import Max
# Create your views here.

def home(request):
        if request.method=='POST':
                postRequest = request.POST
                if 'day_name' in postRequest.keys():
                        form = DayForm(postRequest)
                        if form.is_valid():
                                form.save()
                                return HttpResponseRedirect('/') 
                if 'delete' in postRequest.keys():
                        name_to_delete = postRequest['delete'] #has no attribute cleaned data if I try to clean data
                        day.objects.get(day_name = name_to_delete).delete()
                        return HttpResponseRedirect('/') 

        current_days = day.objects.all()
        day_form = DayForm()
        context = {'day_form': day_form, 'current_days' : current_days}
        return render(request, 'myapp/home.html', context)


def certain_day(request, name):
        current_day_instance = day.objects.get(day_name = name) 
        if request.method=='POST':
                postRequest = request.POST
                if 'workout_name' in postRequest.keys():
                        form = WorkoutForm(postRequest)
                        if form.is_valid():
                                data = form.save(commit=False)
                                data.day = current_day_instance
                                form.save()
                                return HttpResponseRedirect('/day/' + name) 
                
                if 'delete' in postRequest.keys():
                        name_to_delete = postRequest['delete'] #has no attribute cleaned data if I try to clean data
                        workout.objects.get(workout_name = name_to_delete).delete()
                        return HttpResponseRedirect('/day/' + name) 

        current_workouts = workout.objects.filter(day = current_day_instance)
        workout_form = WorkoutForm()
        context = {'workout_form' : workout_form, 'current_workouts': current_workouts, 'name':name} 
        return render(request, 'myapp/certain_day.html', context)


def generic_workout(request, name='dumbell_press'):
        current_workout_instance = workout.objects.get(workout_name = name)
        current_day_name = current_workout_instance.day.day_name  
        if request.method=='POST':
                postRequest = request.POST
                if 'set_num' in postRequest.keys() and 'rep_num' in postRequest.keys() and 'weight' in postRequest.keys() and 'date' in postRequest.keys():
                        form = InfoForm(postRequest)
                        if form.is_valid():
                                data = form.save(commit=False)
                                data.workout = current_workout_instance
                                form.save()
                                return HttpResponseRedirect(name) 
                if 'delete' in postRequest.keys():
                        info_id = postRequest['delete'] #has no attribute cleaned data if I try to clean data
                        item_to_be_deleted = info.objects.get(id = info_id)
                        item_to_be_deleted.deleted = True
                        item_to_be_deleted.save()
                        print(info.objects.get(id=info_id).deleted)
                        return HttpResponseRedirect('/workout/' + name) 
                if 'quick_insert' in postRequest.keys():
                        form = QuickInsertForm(postRequest) #Do I need this?
                        if form.is_valid():     #Do I need this
                                quick_string = request.POST['quick_insert']
                                #\d+-\d+-\d+ errors if you have (digit-digit-digit followed by characters)
                                pattern = re.compile("\d+-\d+-\d+")
                                if (pattern.match(quick_string)):
                                        quick_list = quick_string.split('-')
                                        obj = info()
                                        obj.workout = current_workout_instance
                                        obj.set_num = int(quick_list[0])
                                        obj.rep_num = int(quick_list[1])
                                        obj.weight = int(quick_list[2])
                                        obj.date= date(datetime.today().year, datetime.today().month , datetime.today().day)
                                        obj.save()
                        return HttpResponseRedirect('/workout/' + name)

                #For some reason, if you have a .latest at the end of the conditional clause below, this will give you an error
                #Was working when we used filter, but it not working when we use get
                if 'undo' in postRequest.keys():
                        if info.objects.filter(workout = current_workout_instance, deleted = True):
                                object_to_reappear = info.objects.filter(workout = current_workout_instance, deleted = True).latest('time_modified')
                                object_to_reappear.deleted = False
                                object_to_reappear.save()
                        return HttpResponseRedirect(name) 

                
                                        
        quick_insert_form = QuickInsertForm
        info_form = InfoForm() 
        workouts_completed = info.objects.filter(workout = current_workout_instance, deleted = False).order_by('-date', 'set_num', '-weight')
        #Creates a hashmap in the format of: format = { date1: [list of workouts on date1], date2: [list of workouts on date2]}
        format = {}
        for item in workouts_completed:
                if item.date in format.keys():
                        format[item.date].append(item)
                if item.date not in format.keys():
                        format[item.date] = [item]
                



        context = {'quick_insert_form': quick_insert_form, 'format': format, 'info_form': info_form, 'workouts_completed': workouts_completed, 'name': name, 'current_day_name': current_day_name}
        return render(request, 'myapp/generic_workout.html', context)

#Just a view that shows full current-workout information for a certain day
def full_view(request, name_of_day='Chest'):
        #For ever workout in list of workouts for this day
        format = {}
        workout_dates = {}
        current_day_instance = day.objects.get(day_name = name_of_day) 
        workouts_in_this_day = workout.objects.filter(day = current_day_instance)
        
        #Gives us a dictionary of all the important information for the latest infos
        for current_workout in workouts_in_this_day:
                if (info.objects.filter(workout = current_workout, deleted = False)):
                        latest_date = info.objects.filter(workout = current_workout, deleted = False).order_by('-date').latest('date').date
                        list_of_infos = info.objects.filter(workout = current_workout, deleted = False, date = latest_date).order_by('-date', 'set_num', '-weight') #latest('date')
                        #format[current_workout.workout_name] = list_of_infos 
                        format[current_workout.workout_name] = {latest_date : list_of_infos}
        

        context = {'format': format, 'name_of_day': name_of_day}
        return render(request, 'myapp/full_view.html', context)


        
        

        


    



